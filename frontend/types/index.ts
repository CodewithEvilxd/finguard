export type RiskLevel = "low" | "medium" | "high" | "critical";

export type AlertStatus = "new" | "investigating" | "confirmed_fraud" | "false_positive" | "dismissed";

export interface Transaction {
  id: string;
  transaction_id: string;
  account_id: string;
  amount: number;
  currency: string;
  transaction_type: string;
  channel: string;
  status: string;
  timestamp: string;
  created_at: string;
  risk_score?: number | null;
  risk_level?: RiskLevel | null;
  fraud_probability?: number | null;
  anomaly_score?: number | null;
  rule_score?: number | null;
  model_version?: string | null;
  explanation_payload?: string | null;
  investigation_id?: string | null;
  investigation_status?: string | null;
}

export interface Alert {
  id: string;
  transaction_id: string;
  risk_score: number;
  risk_level: RiskLevel;
  status: AlertStatus;
  trigger_reason: string;
  factors_summary?: string | null;
  created_at: string;
  updated_at: string;
  transaction_amount?: number;
  transaction_currency?: string;
  account_id?: string;
}

export interface InvestigationNote {
  id: string;
  author_id?: string | null;
  note_type: "analyst" | "ai_assistant" | "system";
  content: string;
  created_at: string;
}

export interface Investigation {
  id: string;
  alert_id: string;
  assigned_analyst_id?: string | null;
  status: string;
  priority: string;
  decision?: string | null;
  decision_rationale?: string | null;
  decided_at?: string | null;
  created_at: string;
  updated_at: string;
  alert?: Alert;
  notes: InvestigationNote[];
}

export interface Account {
  id: string;
  account_number: string;
  account_holder: string;
  balance: number;
  currency: string;
  risk_tier: string;
  status: string;
  created_at?: string;
}

export interface AccountRiskProfile {
  account_id: string;
  account_internal_id: string;
  holder_name: string;
  balance: number;
  currency: string;
  risk_tier: string;
  total_transactions: number;
  total_spend: number;
  average_transaction_amount: number;
  max_transaction_amount: number;
  average_risk_score: number;
  peak_risk_score: number;
  high_risk_transactions_count: number;
  total_alerts_count: number;
  created_at?: string;
}

export interface OverviewMetrics {
  total_transactions_24h: number;
  active_alerts_count: number;
  high_risk_count: number;
  critical_risk_count: number;
  pending_investigations: number;
  resolved_today: number;
  mean_resolution_hours: number;
}

export interface RiskTrendPoint {
  timestamp_label: string;
  low_count: number;
  medium_count: number;
  high_count: number;
  critical_count: number;
}

export interface SourceReference {
  document_title: string;
  document_category: string;
  section_title?: string;
  relevance_score: number;
  excerpt: string;
}

export interface AssistantResponse {
  query_id: string;
  response_text: string;
  sources: SourceReference[];
  limitations?: string;
  disclaimer: string;
}

export interface RetrainingMetrics {
  xgboost?: {
    roc_auc?: number;
    pr_auc?: number;
    f1?: number;
    samples?: number;
  };
  isolation_forest?: {
    contamination?: number;
    samples?: number;
  };
  records_trained?: number;
  xgboost_val_auc?: number;
  isolation_forest_anomalies_detected?: number;
  trained_at?: string;
}

export interface RetrainingStatus {
  auto_retraining_enabled: boolean;
  scheduler_interval_hours: number;
  status: string;
  is_running: boolean;
  last_retrained_at?: string | null;
  next_scheduled_run?: string | null;
  total_completed_runs: number;
  latest_metrics?: RetrainingMetrics;
  last_error?: string | null;
}
