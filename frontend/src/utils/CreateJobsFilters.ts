export function CreateJobsFilters() {
    const jobsFilter: Array<string> = [
        "pending",
        "submitted",
        "running",
        "error",
        "failed",
        "succeeded"
    ];
    
    return jobsFilter
}