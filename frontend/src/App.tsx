import React from 'react';
import Container from 'react-bootstrap/Container'
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import { Routes, Route, Outlet } from "react-router-dom";
import 'bootstrap/dist/css/bootstrap.min.css';
import { useTable, Column } from 'react-table';
import Table from 'react-bootstrap/Table';
import './App.css';


class Layout extends React.Component {
  render(): JSX.Element {
    return (
      <div>
        <Navbar bg="light">
          <Container>
            <Navbar.Brand href="/">SnakeMon</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
              <Nav className="me-auto">
                <Nav.Link href="/workflows">Workflows</Nav.Link>
              </Nav>
            </Navbar.Collapse>
          </Container>
        </Navbar>

        {/* An <Outlet> renders whatever child route is currently active,
        so you can think about this <Outlet> as a placeholder for
        the child routes we defined above. */}
        <Outlet />
      </div>
    )
  }
}


interface IWorklowsTableProps {
  columns: Array<Column>,
  data: Array<any>,
}
function WorkflowsTable(props: IWorklowsTableProps): JSX.Element {
  // Makes a react-table table via useTable, see:
  // see https://react-table.tanstack.com/docs/api/useTable

  // useTable complains if accessing via props. so we load into constants
  const columns = props.columns
  const data = props.data

  // Use the state and functions returned from useTable to build your UI
  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  } = useTable({
    columns,
    data,
  })

  // Render the UI for your table
  return (
    // apply the table props
    <Table {...getTableProps()}>
      <thead>
        {// Loop over the header rows
        headerGroups.map(headerGroup => (
          // Apply the header row props
          <tr {...headerGroup.getHeaderGroupProps()}>
            {// Loop over the headers in each row
            headerGroup.headers.map(column => (
              // Apply the header cell props
              <th {...column.getHeaderProps()}>
                {// Render the header
                column.render('Header')}
              </th>
            ))}
          </tr>
        ))}
      </thead>
      {/* Apply the table body props */}
      <tbody {...getTableBodyProps()}>
        {// Loop over the table rows
        rows.map((row, i) => {
          // Prepare the row for display
          prepareRow(row)
          return (
            // Apply the row props
            <tr {...row.getRowProps()}>
              {// Loop over the rows cells
              row.cells.map(cell => {
                // Apply the cell props
                return (
                  <td {...cell.getCellProps()}>
                  {// Render the cell contents
                  cell.render('Cell')}
                  </td>)
              })}
            </tr>
          )
        })}
      </tbody>
    </Table>
  )
}


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
          Header: "Started at",
          accessor: "started_at"
        },
        {
          Header: "Completed at",
          accessor: "completed_at"
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
        <WorkflowsTable columns={this.getColumns()} data={this.state.data}/>
      )
    }
}


interface IHomeProps {}
interface IHomeState {
  message: string
}
class Home extends React.Component<IHomeProps, IHomeState> {
  constructor(props: IHomeProps) {
    super(props);
    this.state = {
      message: "Waiting on response from backend ...",
    };
  }

  componentDidMount() {
    fetch("http://localhost:8000/")
    .then(response => response.json())
    .then(data => {this.setState({message: data.message,})})
  }

  render(): JSX.Element {
    return (
      <div>
        <h1>{this.state.message}</h1>
      </div>
    )
  }
}


class App extends React.Component {
  render(): JSX.Element {
    return (
      <div className="App">
        <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} /> {/* note only home has index */}
          <Route path="workflows" element={<Workflows />} />

          {/* Using path="*"" means "match anything", so this route
                acts like a catch-all for URLs that we don't have explicit
                routes for. */}
          {/* <Route path="*" element={<Home />} /> */}
        </Route>
      </Routes>
      </div>
    )
  }
}

export default App;
