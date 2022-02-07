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
    const [workflow, setWorkflow] = useState<IWorkflow|undefined>(undefined);
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
      }, []) // The empty array ensures the useEffect is only run once

    return(
        <div id="WorkflowDetail" className="p-3">
            {/* <h1>Workflow #{workflowId} details</h1> */}
            <div id="WorkflowDetail-Header">
                <span className="h2">{workflow?.workflow} / </span>
                <span className="h2 fst-italic">{workflow?.name}</span>
            </div>
            <hr/>

            <div id="WorkflowDetail-Body" className="row">

                <div id="WorkflowDetail-General" className="col-4">
                    <div className="card">
                        <div className="card-body">
                        <h5 className="card-title">General</h5>
                        <div className="table-responsive">

                            <table className="table table-borderless">
                            <tbody>{workflow &&
                                Object.entries(workflow).map((item, idx) => (
                                    <tr>
                                        <td>{item[0]}</td>
                                        <td>{item[1]}</td>
                                    </tr>
                                    ))}</tbody>
                            </table>
                        </div>
                        </div>
                    </div>
                </div>

                <div id="WorkflowDetail-Jobs" className="col-8">
                    <div className="card">
                        <div className="card-body">
                            <h5 className="card-title">Jobs</h5>
                            <p>Jobs</p>
                        </div>
                    </div>
                </div>

                

            </div>

        </div>
    )
}
