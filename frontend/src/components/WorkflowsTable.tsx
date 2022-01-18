import { Column, usePagination, useSortBy, useTable } from 'react-table';
import { Badge, Form, Pagination, Table} from 'react-bootstrap';

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
                    } else if (cell.value === "Error") {
                      cellContent = (
                        <Badge bg="danger">{cell.render("Cell")}</Badge>
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
      <div style={{float: "right", display: "flex", flexDirection: "row", marginTop: "2%", marginRight: "2%", whiteSpace: "nowrap"}}>
          <span style={{margin: "2%"}}>
            Page{' '}
            <strong>
              {pageIndex + 1} of {pageOptions.length}
            </strong>
          </span>
        <Form.Select style={{height: "38px", width: "120px", marginRight: "2%"}}
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
        </Form.Select>
        <Pagination>
          <Pagination.First onClick={() => gotoPage(0)} disabled={!canPreviousPage}/>
          <Pagination.Prev onClick={() => previousPage()} disabled={!canPreviousPage}/>
        <input
            // type="number"
            defaultValue={pageIndex + 1}
            onChange={e => {
              const page = e.target.value ? Number(e.target.value) - 1 : 0
              gotoPage(page)
            }}
            style={{height: "38px", width: '50px'}}
          />
          <Pagination.Next onClick={() => nextPage()} disabled={!canNextPage}/>
          <Pagination.Last onClick={() => gotoPage(pageCount - 1)} disabled={!canNextPage}/>
        </Pagination>
      </div>
      </>
    )
  }

export default WorkflowsTable;
