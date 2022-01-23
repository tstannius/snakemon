import React, { useEffect, useState } from 'react';
import { Routes, Route } from "react-router-dom";
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

import {
  Home,
  Signin,
  Signup,
  Test,
  WorkflowDetail,
  Workflows
} from "./views";
import { NavBar } from './components'
import { authProvider } from "./utils/auth";


export default function App(): JSX.Element {
  const [user, setUser] = useState<null|string>(null); // Todo - get user, instead of reset

  useEffect(() => {
    authProvider.TestToken().then((result) => {
        setUser(result);
    });
  }, [])

  return (
    <div className="App">
      <Routes>
      <Route path="/" element={<NavBar user={user} setUser={setUser} />}>
        <Route index element={<Home />} /> {/* note only home has index */}
        <Route path="/workflows" element={<Workflows />} />
          {/* TODO: consider other placement */}
          <Route path="/workflows/:workflowId" element={<WorkflowDetail />} />
        <Route path="/signin" element={<Signin user={user} setUser={setUser} />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/test" element={<Test />} />
        {/* Using path="*"" means "match anything", so this route
              acts like a catch-all for URLs that we don't have explicit
            routes for. */}
        <Route path="*" element={<Home />}/>
      </Route>
    </Routes>
    </div>
  )
}
