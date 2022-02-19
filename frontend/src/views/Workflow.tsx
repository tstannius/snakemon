import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from "react-router-dom";

import { apiUrl } from '../env';

import { CommentList, WorkflowDetail } from "../components"
import { IWorkflow } from "../interfaces"



export default function Workflow(): JSX.Element {
    let [workflow, setWorkflow] = useState<IWorkflow|undefined>(undefined);
    let { workflowId } = useParams();
    let navigate = useNavigate();

    function getWorkflow(): void {
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
        });
    }


    useEffect(() => {
        getWorkflow();
      }, []) // The empty array ensures the useEffect is only run once

    return(
        <div id="Workflow" className="p-3">
            <div id="Workflow-Header">
                <span className="h2">{workflow?.workflow} / </span>
                <span className="h2 fst-italic">{workflow?.name}</span>
            </div>
            <hr/>

            <div id="Workflow-Body-Top" className="row pb-3">
                <div id="Workflow-General" className="col-4">
                    <div className="card">
                        <div className="card-body">
                        <h5 className="card-title">General</h5>
                            {workflow &&
                                <WorkflowDetail workflow={workflow}/>
                            }
                        </div>
                    </div>
                </div>

                <div id="Workflow-Jobs" className="col-8">
                    <div className="card">
                        <div className="card-body">
                            <h5 className="card-title">Jobs</h5>
                            <p>Jobs</p>
                        </div>
                    </div>
                </div>
            </div>

            <div id="Workflow-Body-Mid" className="row">
                <div id="Workflow-Comments" className="col-4">
                    <div className="card">
                        <div className="card-body">
                            <h5 className="card-title">Comments</h5>
                            <CommentList workflowId={workflowId}/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
