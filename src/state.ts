import { RequestState, AuditLog } from './types';

class StateStore {
  private states: Map<string, RequestState> = new Map();

  getState(requestId: string): RequestState | undefined {
    return this.states.get(requestId);
  }

  setState(requestId: string, state: RequestState): void {
    this.states.set(requestId, state);
  }

  addAuditLog(requestId: string, stage: string, details: string): void {
    const state = this.states.get(requestId);
    if (state) {
      const log: AuditLog = {
        timestamp: new Date().toISOString(),
        requestId,
        stage,
        details,
      };
      state.auditLogs.push(log);
      console.log(`[AUDIT] ${log.timestamp} | ${requestId} | ${stage} | ${details}`);
    }
  }
}

export const stateStore = new StateStore();
