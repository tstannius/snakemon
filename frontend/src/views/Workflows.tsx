import React from 'react';
import { Column } from 'react-table';
import { Card } from 'react-bootstrap';
import { WorkflowsTable } from "../components"

interface IWorkflowsProps {}
interface IWorkflowsState {
  data: any[]
}
class Workflows extends React.Component<IWorkflowsProps, IWorkflowsState> {
  constructor(props: IWorkflowsProps) {
    super(props);
    this.state = {
      data: [],
    };
  }

  // TODO:
  // move elsewhere
  // should ideally use React.useMemo(), find out how
  getColumns(): Array<Column> {
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
    return(columns)
  }

  componentDidMount() {
    fetch("http://localhost:8000/workflows", {method: "GET", mode: "cors"})
    .then(response => response.json())
    .then(data => {
      this.setState({
        data: data
      })
    })
  }

  render(): JSX.Element {
    return (
      <Card body style={{margin: "3%"}}>
        <Card.Body>
          <WorkflowsTable columns={this.getColumns()} data={this.state.data}/>
        </Card.Body>
      </Card>
      )
    }
}

export default Workflows;
