import React from 'react';
import { Routes, Route } from "react-router-dom";
import 'bootstrap/dist/css/bootstrap.min.css';
import { Home, Signin, Signup, Workflows } from "./views";
import { NavBar } from './components'
import './App.css';



class App extends React.Component {
  render(): JSX.Element {
    return (
      <div className="App">
        <Routes>
        <Route path="/" element={<NavBar />}>
          <Route index element={<Home />} /> {/* note only home has index */}
          <Route path="workflows" element={<Workflows />} />
          <Route path="/signin" element={<Signin />} />
          <Route path="/signup" element={<Signup />} />

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
