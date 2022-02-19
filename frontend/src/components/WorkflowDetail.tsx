import React from 'react';

import { IWorkflow } from "../interfaces"

interface IWorkflowDetailProps {
    workflow: IWorkflow
}

export default function WorkflowDetail(props: IWorkflowDetailProps): JSX.Element {
    return(
        <div id="WorkflowDetail" className="table-responsive">
            <table className="table table-borderless">
                <tbody>{Object.entries(props.workflow).map((item, idx) => (
                    <tr key={idx}>
                        <td>{item[0]}</td>
                        <td>{item[1]}</td>
                    </tr>
                    ))
                }</tbody>
            </table>
        </div>
    )
}
