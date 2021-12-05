import React, { CSSProperties } from 'react';
import Container from 'react-bootstrap/Container'
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import { Routes, Route, Outlet } from "react-router-dom";
import 'bootstrap/dist/css/bootstrap.min.css';
import { Column, usePagination, useSortBy, useTable } from 'react-table';
import { Badge, Card, Table} from 'react-bootstrap';
import './App.css';
import { ReactComponent as Logo } from './assets/favicon.svg';


class Layout extends React.Component {
  render(): JSX.Element {
    return (
      <div>
        <Navbar bg="light" sticky="top">
          <Container>
            <Navbar.Brand href="/">
            <Logo />{' '}
              SnakeMon</Navbar.Brand>
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
    // rows, // we use page instead
    prepareRow,
    page,
    canPreviousPage,
    canNextPage,
    pageOptions,
    pageCount,
    gotoPage,
    nextPage,
    previousPage,
    setPageSize,
    state: { pageIndex, pageSize },
  } = useTable(
    {
      columns,
      data,
      initialState: { pageIndex: 0 },
    },
  useSortBy,
  usePagination
  )

  // Render the UI for your table
  return (
    <>
    {/* apply the table props */}
    <div style={{minHeight: "460px", verticalAlign: "top"}}>
    <Table {...getTableProps()}>
      <thead>
        {// Loop over the header rows
        headerGroups.map(headerGroup => (
          // Apply the header row props
          <tr {...headerGroup.getHeaderGroupProps()}>
            {// Loop over the headers in each row
            headerGroup.headers.map(column => {
              return (
                
              // Apply the header cell props
              <th {...column.getHeaderProps(column.getSortByToggleProps())}>
                {// Render the header
                column.render('Header')}
                {/* Add a sort direction indicator */}
                {/* see:
                https://github.com/ggascoigne/react-table-example
                https://github.com/DefinitelyTyped/DefinitelyTyped/blob/master/types/react-table/Readme.md
              */}
                <span>
                {column.isSorted
                  ? column.isSortedDesc
                  ? ' \u2193'
                  : ' \u2191'
                  : ' \u2193\u2191'}
                </span>
              </th>
            )}
          )}</tr>
          ))}
      </thead>
      {/* Apply the table body props */}
      <tbody {...getTableBodyProps()}>
        {// Loop over the table rows
        page.map((row, i) => {
          // Prepare the row for display
          prepareRow(row)
          return (
            // Apply the row props
            <tr {...row.getRowProps()}>
              {// Loop over the rows cells
              row.cells.map(cell => {
                console.log(cell.column.Header);
                var cellContent = cell.render("Cell");

                if (cell.column.Header === "Status") {
                  if (cell.value === "Done") {
                    cellContent = (
                      <Badge bg="success">{cell.render("Cell")}</Badge>
                    );
                  } else if (cell.value === "Running") {
                    cellContent = (
                      <Badge bg="warning">{cell.render("Cell")}</Badge>
                    );
                  } else {
                    cellContent = (
                      <Badge bg="secondary">{cell.render("Cell")}NA</Badge>
                    );
                  }
                }
                
                // Apply the cell props
                return (
                  <td {...cell.getCellProps()}>
                  {// Render the cell contents
                  cellContent}
                  </td>)
              })}
            </tr>
          )
        })}
      </tbody>
    </Table>
    </div>
      {/* Pagination can be built however you'd like. 
      This is just a very basic UI implementation: */}
      <div className="pagination" style={{float: "right"}}>
        <select
          value={pageSize}
          onChange={e => {
            setPageSize(Number(e.target.value))
          }}
        >
          {[10, 20, 30, 40, 50].map(pageSize => (
            <option key={pageSize} value={pageSize}>
              Show {pageSize}
            </option>
          ))}
        </select>
        <span>
          Page{' '}
          <strong>
            {pageIndex + 1} of {pageOptions.length}
          </strong>
          {' '}
        </span>{' '}
        <button onClick={() => gotoPage(0)} disabled={!canPreviousPage}>
          {'<<'}
        </button>{' '}
        <button onClick={() => previousPage()} disabled={!canPreviousPage}>
          {'<'}
        </button>{' '}
        <input
            // type="number"
            defaultValue={pageIndex + 1}
            onChange={e => {
              const page = e.target.value ? Number(e.target.value) - 1 : 0
              gotoPage(page)
            }}
            style={{ width: '50px' }}
          />
        <button onClick={() => nextPage()} disabled={!canNextPage}>
          {'>'}
        </button>{' '}
        <button onClick={() => gotoPage(pageCount - 1)} disabled={!canNextPage}>
          {'>>'}
        </button>{' '}
      </div>
      </>
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
      <Card style={{margin: "3%"}}>
        <Card.Body>
          <WorkflowsTable columns={this.getColumns()} data={this.state.data}/>
        </Card.Body>
      </Card>
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
    const style = {
      marginLeft: "auto",
      marginRight: "auto",
  } as CSSProperties;

    return (
      <div className="centered">
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
