import React, { useCallback, useEffect, useRef, useState, useMemo } from 'react';
import InputGroup from "react-bootstrap/InputGroup"
import Form from 'react-bootstrap/Form';
import FormControl from 'react-bootstrap/FormControl';

import { WorkflowsTable } from "../components"
import { apiUrl } from '../env';


export default function Workflows(): JSX.Element {
  const [workflowsData, setWorkflowsData] = useState<Array<any>>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [pageCount, setPageCount] = useState<number>(0);
  const fetchIdRef = useRef<number>(0);
  const skipPageResetRef = React.useRef(false);

  const [searchString, setSearchString] = useState<string>("");

  const handleChangeSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchString(e.currentTarget.value);
  }

  // This will get called when the table needs new data
  // useCallback ensures a new function is not generated
  const fetchData = useCallback((pageIndex: number, pageSize: number, searchString: string): void => {
    // set ref to prevent page reset
    // cf. react-table.tanstack.com/docs/faq#how-do-i-stop-my-table-state-from-automatically-resetting-when-my-data-changes
    skipPageResetRef.current = true;
    
    // give this fetch an id
    const fetchId = ++fetchIdRef.current;

    setLoading(true);

    if (fetchId === fetchIdRef.current) {
      const startRow = pageSize * pageIndex;

      const params = new URLSearchParams({
        offset: startRow.toString(),
        limit: pageSize.toString()
      })
      
      if (searchString) {
        params.append("query", searchString.trim())
      }
        
      // leading '?' query parameters
      const searchParams = "?" + params.toString();

      // set query params like so: https://stackoverflow.com/questions/35038857/setting-query-string-using-fetch-get-request
      fetch(`${apiUrl}/workflows` + searchParams,
        { method: "GET", mode: "cors" })
        .then(response => response.json())
        .then(data => {
          // server handles slice and calculates total page count
          setWorkflowsData(data.workflows);
          setPageCount(data.page_count);
        });
      setLoading(false);
    }
  }, [])

  useEffect(() => {
    skipPageResetRef.current = false;
  }, [workflowsData]);


  // Column headers and accessors for the table to be generated
  const columns = useMemo(
    () => [
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
    ],
    []
  );

  return (
    <div id="WorkflowsOverviewContainer" className="p-4">
      <div className="card">
        <div className="card-body">
        <h5 className="card-title">Workflows</h5>
          <div id="WorkflowsOverview-Toolbar" className="d-flex flex-row mb-3">
                  {/* right placement is due to me-auto in previous flex item, see
                  https://getbootstrap.com/docs/5.0/utilities/flex/#auto-margins */}
                  <div id="WorkflowsOverview-Toolbar-Filters" className="me-auto">
                  </div>
                  <div id="WorkflowsOverview-Toolbar-Search">
                      <Form>
                          <InputGroup>
                              <FormControl
                                  // required
                                  type="text"
                                  placeholder="Search ..."
                                  value={searchString}
                                  onChange={handleChangeSearch}
                              />
                          </InputGroup>
                      </Form>
                  </div>
              </div>
          <WorkflowsTable 
            columns={columns} 
            data={workflowsData}
            callbackFetchData={fetchData}
            skipPageResetRef={skipPageResetRef}
            controlledPageCount={pageCount}
            searchString={searchString}
            loading={loading}
            />
        </div>
      </div>
    </div>
  )
}
