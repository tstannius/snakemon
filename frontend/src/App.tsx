import React from 'react';
import { Routes, Route } from "react-router-dom";
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

import {
  Home,
  Signin,
  Signup,
  Test,
  Workflow,
  Workflows
} from "./views";
import { NavBar } from './components'
import { AuthProvider } from './hooks';


export default function App(): JSX.Element {
  return (
    <div className="App">
      <AuthProvider>
        <Routes>
        <Route path="/" element={<NavBar />}>
          <Route index element={<Home />} /> {/* note only home has index */}
          <Route path="/workflows" element={<Workflows />} />
            {/* TODO: consider other placement */}
            <Route path="/workflows/:workflowId" element={<Workflow />} />
          <Route path="/signin" element={<Signin />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/test" element={<Test />} />
          {/* Using path="*"" means "match anything", so this route
                acts like a catch-all for URLs that we don't have explicit
              routes for. */}
          <Route path="*" element={<Home />}/>
        </Route>
      </Routes>
    </AuthProvider>
    </div>
  )
}
