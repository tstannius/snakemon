
enum WorkflowStatus {
    Running = "Running",
    Done = "Done",
    Error = "Error",
}

export interface IWorkflow {
    workflow: string;
    name: string;
    id: number;
    status: WorkflowStatus;
    done: number;
    total: number;
    started_at: string;
    completed_at: string;
    last_update_at: string;
    timestamp: string;
}
