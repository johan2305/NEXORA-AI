from pydantic import BaseModel


class AnalyticsSummary(BaseModel):
    total_tasks: int
    tasks_by_status: dict[str, int]
    tasks_by_created_by: dict[str, int]
    total_customers: int
    total_projects: int
    total_automations: int
    automation_executions_success: int
    automation_executions_failed: int
    ai_requests_total: int
    ai_avg_latency_ms: float | None
    estimated_hours_saved: float