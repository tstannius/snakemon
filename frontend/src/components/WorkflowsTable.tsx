import React, { useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import { Column, useAsyncDebounce, useFilters, usePagination, useSortBy, useTable } from 'react-table';

import { Badge, Form, Pagination, Table} from 'react-bootstrap';

interface IWorklowsTableProps {
    columns: Array<Column>,
    data: Array<any>,
    callbackFetchData: (pageIndex: number, pageSize: number, searchString: string) => void,
    skipPageResetRef: React.MutableRefObject<boolean>
    controlledPageCount: number,
    searchString: string,
    loading: boolean, // TODO: add fancy loading indicator with fade
  }

function WorkflowsTable(props: IWorklowsTableProps): JSX.Element {
    // Makes a react-table table via useTable, see:
    // see https://react-table.tanstack.com/docs/api/useTable
    let navigate = useNavigate();
  
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
      // Get the state from the instance
      state: { pageIndex, pageSize },
    } = useTable(
      {
        columns: props.columns,
        data: props.data,
        initialState: { pageIndex: 0, pageSize: 30 },
        // Tell the usePagination
        // hook that we'll handle our own data fetching
        // This means we'll also have to provide our own
        // pageCount.
        manualPagination: true,
        pageCount: props.controlledPageCount,
        // stop auto updating anything when fetching data
        // cf. react-table.tanstack.com/docs/faq#how-do-i-stop-my-table-state-from-automatically-resetting-when-my-data-changes
        autoResetPage: !props.skipPageResetRef.current,
        autoResetExpanded: !props.skipPageResetRef.current,
        autoResetGroupBy: !props.skipPageResetRef.current,
        autoResetSelectedRows: !props.skipPageResetRef.current,
        autoResetSortBy: !props.skipPageResetRef.current,
        autoResetFilters: !props.skipPageResetRef.current,
        autoResetRowState: !props.skipPageResetRef.current,
        // manual filtering for server side filtering
        // manualFilters: true,
        searchString: props.searchString
      },
    useFilters,
    useSortBy,
    usePagination,
    )

    // Debounce our onFetchData call for 100ms
   const onFetchDataDebounced = useAsyncDebounce(props.callbackFetchData, 200)

    // Listen for changes in pagination or searchString and use the state to fetch our new data
    useEffect(() => {
      onFetchDataDebounced(pageIndex, pageSize, props.searchString );
    }, [onFetchDataDebounced, pageIndex, pageSize, props.searchString ]);
  
    // Render the table UI
    return (
      <>
      {/* apply the table props */}
      <div id="WorkflowsTableContainer" style={{verticalAlign: "top"}}>
      <Table id="WorkflowsTable" hover responsive {...getTableProps()}>
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
              <tr {...row.getRowProps()} onClick={() => navigate(`/workflows/${row.values.id}`)}>
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
            className="text-center"
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
