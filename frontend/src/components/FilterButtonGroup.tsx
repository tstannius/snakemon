import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';
import ToggleButton from 'react-bootstrap/ToggleButton';
import ToggleButtonGroup from 'react-bootstrap/ToggleButtonGroup';

import { ReactComponent as Funnel } from '../assets/funnel.svg';
import { ReactComponent as FunneFill } from '../assets/funnel-fill.svg';

import { IJobsSummary } from '../interfaces/IJobsSummary';
import { CreateJobsFilters } from '../utils/CreateJobsFilters';

interface IFilterButtonGroup {
    jobsSummary: IJobsSummary;
    jobsFilters: Array<string>;
    callbackUpdateFilters: (filter: any) => void;
}
// https://stackoverflow.com/questions/71345520/modify-only-one-field-of-the-interface-with-the-usestate

export function FilterButtonGroup(props: IFilterButtonGroup) {
    let [filtering, setFiltering] = useState<boolean>(false);
    /*
     * The second argument that will be passed to
     * `handleChange` from `ToggleButtonGroup`
     * is the SyntheticEvent object, but we are
     * not using it, so we will omit it.
     */
    const handleChange = (val: Array<string>) => {
        // call the parent set hook with new value
        // props.callbackUpdateFilters(val)
        const jobsFiltersBase = CreateJobsFilters();
        if (!filtering && (val.length === (jobsFiltersBase.length - 1))) {
            const diff = jobsFiltersBase.filter(x => !val.includes(x));
            props.callbackUpdateFilters(diff);
        } else {
            props.callbackUpdateFilters(val);
        }
        if (val.length !== jobsFiltersBase.length) {
            setFiltering(true);
        } else {
            setFiltering(false);
        }
    };

    const setFilters = () => {
        if (props.jobsFilters.length === 0) {
            props.callbackUpdateFilters(CreateJobsFilters());
            setFiltering(false);
        } else {
            props.callbackUpdateFilters([]);
            setFiltering(true);
        }
    }

    return (
        <div className="text-nowrap">
            <ToggleButtonGroup type="checkbox" value={props.jobsFilters} onChange={handleChange}>
                <Button id="btn-filter" variant="" className="btn-secondary" onClick={setFilters}>
                    {filtering ?
                        <FunneFill /> :
                        <Funnel />
                    }
                </Button>
                <ToggleButton id="btn-pending" variant="" className="btn-filter pending" value={"pending"}>
                    {props.jobsSummary.pending} pending
                </ToggleButton>
                {/* submitted only relevant if on cluster */}
                <ToggleButton id="btn-submitted" variant="" className="btn-filter submitted" value={"submitted"}>
                    {props.jobsSummary.submitted} submitted
                </ToggleButton>
                <ToggleButton id="btn-running" variant="" className="btn-filter running" value={"running"}>
                    {props.jobsSummary.running} running
                </ToggleButton>
                <ToggleButton id="btn-error" variant="" className="btn-filter error" value={"error"}>
                    {props.jobsSummary.error} error
                </ToggleButton>
                <ToggleButton id="btn-failed" variant="" className="btn-filter failed" value={"failed"}>
                    {props.jobsSummary.failed} failed
                </ToggleButton>
                <ToggleButton id="btn-succeeded" variant="" className="btn-filter succeeded" value={"succeeded"}>
                    {props.jobsSummary.succeeded} succeeded
                </ToggleButton>
            </ToggleButtonGroup>
        </div>
    );
}
