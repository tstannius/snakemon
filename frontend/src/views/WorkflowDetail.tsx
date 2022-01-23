import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from "react-router-dom";

import { apiUrl } from '../env';

enum WorkflowStatus {
    Running = "Running",
    Done = "Done",
    Error = "Error",
}

interface IWorkflow {
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



export default function WorkflowDetail(): JSX.Element {
    const [workflow, setWorkflow] = useState<IWorkflow|null>(null);
    let { workflowId } = useParams();
    let navigate = useNavigate();

    useEffect(() => {
        const request = new Request(`${apiUrl}/workflows/${workflowId}`, {
            method: 'GET',
            credentials: 'include', // necessary for cookies
          });

        fetch(request)
            .then((response) => {
                if (response.status === 200) {
                    response.json()
                        .then(data => {
                            setWorkflow(data)
                        })
                } else if ((response.status >= 400) && (response.status <= 500)) {
                    response.json()
                        .then(data => {
                            // TODO: don't redirect, but use history
                            console.log(data.detail)
                            navigate("/workflows");
                        })
                }
        })
      }, [])

    return(
        <div id="WorkflowDetail">
            <h1>Workflow #{workflowId} details</h1>
            {
                workflow &&
                    Object.entries(workflow).map((item, idx) => (
                        <li key={idx}>
                            <span>{item[0]}: {item[1]}</span>
                        </li>
                    ))
            }
        </div>
    )
}
