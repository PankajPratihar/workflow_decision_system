export type WorkflowAction = 'approve' | 'reject' | 'retry' | 'manual_review';

export interface WorkflowRule {
  condition: string;
  action: WorkflowAction;
  reason?: string;
}

export interface WorkflowConfig {
  id: string;
  rules: WorkflowRule[];
}

export interface WorkflowRequest {
  requestId: string;
  workflowId: string;
  payload: any;
}

export interface AuditLog {
  timestamp: string;
  requestId: string;
  stage: string;
  details: string;
}

export interface RequestState {
  requestId: string;
  status: 'PENDING' | 'PROCESSING' | 'COMPLETED' | 'FAILED';
  result?: any;
  auditLogs: AuditLog[];
}
