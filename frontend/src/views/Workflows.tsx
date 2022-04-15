import React, { useEffect, useState } from 'react';
import { Column } from 'react-table';
import { Card } from 'react-bootstrap';
import { WorkflowsTable } from "../components"


export default function Workflows(): JSX.Element {
  let [workflowsData, setWorkflowsData] = useState<Array<any>>([]);

  useEffect(() => {
    fetch("http://localhost:8000/workflows/", { method: "GET", mode: "cors" })
      .then(response => response.json())
      .then(data => {
        setWorkflowsData(data);
      })
  }, []) // The empty array ensures the useEffect is only run once

  /**
   * Return array of column objects for creating react table
   * TODO:
   * - should ideally use React.useMemo(), find out how
   * - consider moving elsewhere
   * 
   * @returns {Array<Column>} Column headers and accessors for the table to be generated
   */
  function getColumns(): Array<Column> {
    const columns = [
      {
        Header: "ID",
        accessor: "id"
      },
      {
        Header: "Workflow",
        accessor: "workflow"
      },
      {
        Header: "Name",
        accessor: "name"
      },
      {
        Header: "Status",
        accessor: "status"
      },
      {
        Header: "Done",
        accessor: "done"
      },
      {
        Header: "Total",
        accessor: "total"
      },
      {
        Header: "Last update at",
        accessor: "last_update_at"
      },
    ];
    return (columns)
  }

  return (
    <div id="WorkflowsTableContainer">
      <Card body style={{ margin: "3%" }}>
        <Card.Body>
          <WorkflowsTable columns={getColumns()} data={workflowsData} />
        </Card.Body>
      </Card>
    </div>
  )
}
