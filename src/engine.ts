import { WorkflowConfig, WorkflowRequest, WorkflowAction, RequestState } from './types';
import { stateStore } from './state';
import workflowConfig from './config/workflow.json';

export class WorkflowEngine {
  private configs: WorkflowConfig[] = (workflowConfig as any).workflows;

  async processRequest(request: WorkflowRequest): Promise<RequestState> {
    // 1. Idempotency Check
    const existingState = stateStore.getState(request.requestId);
    if (existingState) {
      stateStore.addAuditLog(request.requestId, 'IDEMPOTENCY', 'Duplicate request detected, returning existing state');
      return existingState;
    }

    // 2. Initialize State
    const newState: RequestState = {
      requestId: request.requestId,
      status: 'PROCESSING',
      auditLogs: [],
    };
    stateStore.setState(request.requestId, newState);
    stateStore.addAuditLog(request.requestId, 'INITIALIZATION', `Starting workflow: ${request.workflowId}`);

    try {
      // 3. Find Workflow
      const config = this.configs.find(c => c.id === request.workflowId);
      if (!config) {
        throw new Error(`Workflow ${request.workflowId} not found`);
      }

      // 4. Evaluate Rules
      const decision = this.evaluateRules(config, request.payload);
      stateStore.addAuditLog(request.requestId, 'DECISION', `Rule evaluation result: ${decision.action}`);

      // 5. Execute Stage
      await this.executeStage(request, decision.action);

      // 6. Finalize
      newState.status = 'COMPLETED';
      newState.result = { action: decision.action, reason: decision.reason };
      stateStore.addAuditLog(request.requestId, 'COMPLETION', 'Workflow finished successfully');

    } catch (error: any) {
      newState.status = 'FAILED';
      newState.result = { error: error.message };
      stateStore.addAuditLog(request.requestId, 'ERROR', error.message);
    }

    return newState;
  }

  private evaluateRules(config: WorkflowConfig, payload: any): { action: WorkflowAction, reason?: string } {
    for (const rule of config.rules) {
      if (this.checkCondition(rule.condition, payload)) {
        return { action: rule.action, reason: rule.reason };
      }
    }
    return { action: 'manual_review', reason: 'No rules matched' };
  }

  private checkCondition(condition: string, payload: any): boolean {
    // Simple expression evaluator for demo purposes
    // In a real system, use a safe expression parser
    try {
      const keys = Object.keys(payload);
      const values = Object.values(payload);
      const fn = new Function(...keys, `return ${condition}`);
      return fn(...values);
    } catch (e) {
      return false;
    }
  }

  private async executeStage(request: WorkflowRequest, action: WorkflowAction): Promise<void> {
    if (action === 'retry') {
      await this.simulateExternalCallWithRetry(request);
    } else {
      // Other stages might involve external integrations
      stateStore.addAuditLog(request.requestId, 'EXECUTION', `Executing ${action} logic`);
    }
  }

  private async simulateExternalCallWithRetry(request: WorkflowRequest, attempt = 1): Promise<void> {
    const maxAttempts = 3;
    stateStore.addAuditLog(request.requestId, 'EXTERNAL_CALL', `Attempt ${attempt} of ${maxAttempts}`);

    // Simulate failure 70% of the time for first 2 attempts
    const shouldFail = attempt < maxAttempts && Math.random() < 0.7;

    if (shouldFail) {
      stateStore.addAuditLog(request.requestId, 'RETRY', `External call failed, retrying in 1s...`);
      await new Promise(resolve => setTimeout(resolve, 1000));
      return this.simulateExternalCallWithRetry(request, attempt + 1);
    }

    stateStore.addAuditLog(request.requestId, 'EXTERNAL_CALL', 'External call succeeded');
  }
}

export const workflowEngine = new WorkflowEngine();
