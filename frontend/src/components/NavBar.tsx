import React from 'react';
import { Link, Outlet } from "react-router-dom";
import { useNavigate } from 'react-router';
import Container from 'react-bootstrap/Container'
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';

import Logo from "./Logo";
import { useAuth } from "../hooks"



function NavBar(): JSX.Element {
    let navigate = useNavigate();
    let auth = useAuth()

    return (
      <div>
        {/* font-size 5 across the navbar */}
        <Navbar bg="light" sticky="top" className="fs-5">
          {/* Container will center the contents of the navbar */}
          <Container>
            <div id="NavbarContainer-left" className="d-flex flex-row">
              <div id="NavbarBrand" className="d-flex p-2 me-3">
                <Logo />
              </div>
              <Navbar.Toggle aria-controls="basic-navbar-nav" />
              <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="me-auto">
                  <Link className="text-decoration-none me-3" 
                        style={{"color": "gray"}} 
                        to="/workflows">Workflows</Link>
                </Nav>
                <Nav className="me-auto">
                  <Link className="text-decoration-none me-3"
                        style={{"color": "gray"}} 
                        to="/test">Test</Link>
                </Nav>
              </Navbar.Collapse>
            </div>
            
            <div id="NavbarContainer-right" className="d-flex flex-row">
              <Navbar.Collapse className="justify-content-end">
                  {/* conditionally show sign in / sign up */}
                  {/* conditionally show logged in as */}
                  { auth.user ?
                    <div id ="ProfileNavbar-loggedIn">
                      {/* TODO: Show photo */}
                      <span className="align-middle text-center p-2">
                        Hello, {auth.user}!
                      </span>
                      <button className="btn btn-link" style={{"color": "var(--sm-green-dark"}}
                        onClick={() => {
                          auth.signout(() => navigate("/"))
                        }}>
                        Sign out
                      </button>
                    </div>
                  :
                    <div id="ProfileNavbar-loggedOut">
                      <Link className="btn btn-primary" 
                        style={{"backgroundColor": "var(--sm-green-bright", "borderColor": "var(--sm-green-bright"}} 
                        to="/signin">Sign in</Link>
                      <Link className="btn btn-link" style={{"color": "var(--sm-green-dark"}}
                          to="/signup">Sign up</Link>
                    </div>
                  }
              </Navbar.Collapse>
              <Navbar.Toggle />
            </div>
          </Container>
        </Navbar>

        {/* An <Outlet> renders whatever child route is currently active,
        so you can think about this <Outlet> as a placeholder for
        the child routes we defined above. */}
        <Outlet />
      </div>
    )
    
  };

export default NavBar;