import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from "react-router-dom";
import Button from 'react-bootstrap/Button';
import InputGroup from "react-bootstrap/InputGroup"
import Form from 'react-bootstrap/Form';
import FormControl from 'react-bootstrap/FormControl';

import { IJobsSummary } from '../interfaces/IJobsSummary';
import { CreateJobsFilters } from '../utils/CreateJobsFilters';
import { FilterButtonGroup } from './FilterButtonGroup';

import { apiUrl } from '../env';




export default function JobsOverview(): JSX.Element {
    let [jobsSummary, setJobsSummary] = useState<IJobsSummary | undefined>(undefined);
    let [jobsFilters, setJobsFilters] = useState<Array<string>>(CreateJobsFilters());
    let [searchString, setSearchString] = useState<string>("");
    let { workflowId } = useParams();
    let navigate = useNavigate();

    function getJobsSummary(): void {
        const request = new Request(`${apiUrl}/jobs/stats/?workflow_id=${workflowId}`, {
            method: 'GET',
            credentials: 'include', // necessary for cookies
        });
        fetch(request)
            .then((response) => {
                if (response.status === 200) {
                    response.json()
                        .then(data => {
                            console.log(data);
                            setJobsSummary(data)
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
        getJobsSummary();
        console.log(jobsFilters)
    }, []) // The empty array ensures the useEffect is only run once

    return (
        <div id="JobOverview">
            {/* TODO: Tips on UX
            https://ux.stackexchange.com/questions/99330/color-selection-according-to-status
             */}
            <div id="JobOverview-Toolbar" className="d-flex flex-row mb-3">
                <div id="JobOverview-Toolbar-Filters" className="me-auto">
                    {jobsSummary &&
                        // text-center aligns button group in center
                        <FilterButtonGroup
                            jobsSummary={jobsSummary}
                            jobsFilters={jobsFilters}
                            callbackUpdateFilters={setJobsFilters}
                        />
                    }
                </div>
                {/* right placement is due to me-auto in previous flex item, see
                https://getbootstrap.com/docs/5.0/utilities/flex/#auto-margins */}
                <div id="JobOverview-Toolbar-Search">
                    <Form>
                        <InputGroup>
                            <FormControl
                                // required
                                type="text"
                                placeholder="Search ..."
                                value={searchString}
                                // TODO: consider if this inline func is inefficient
                                onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                                    setSearchString(e.currentTarget.value)
                                }
                                }
                            />
                        </InputGroup>
                    </Form>
                </div>
            </div>
            <p>Placeholder for table</p>
            <p>See feedback notes for todo.</p>
            <Button onClick={() => console.log(jobsFilters)}>Console log</Button>
        </div>
    )
}
