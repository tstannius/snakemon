import React from 'react';
import { Outlet } from "react-router-dom";
import Container from 'react-bootstrap/Container'
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import { ReactComponent as Logo } from '../assets/favicon.svg';

class NavBar extends React.Component {
    render(): JSX.Element {
      return (
        <div>
          <Navbar bg="light" sticky="top">
            {/* Container will center the contents of the navbar */}
            <Container>
              <div id="NavbarContainer-left" className="d-flex flex-row">
                <Navbar.Brand href="/">
                <Logo />{' '}
                  SnakeMon</Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                  <Nav className="me-auto">
                    <Nav.Link href="/workflows">Workflows</Nav.Link>
                  </Nav>
                </Navbar.Collapse>
              </div>
              <div id="NavbarContainer-right" className="d-flex flex-row">
                <Navbar.Collapse className="justify-content-end">
                  {/* <Navbar.Text> */}
                    {/* conditionally show sign in / sign up */}
                    {/* conditionally show logged in as */}
                    <div id="ProfileNavbar-loggedOut">
                      <a className="btn btn-primary" 
                        style={{"backgroundColor": "var(--sm-green-bright", "borderColor": "var(--sm-green-bright"}} 
                        href="/signin">Sign in</a>
                      {/* background-color: var(--sm-green-dark); */}
                      <a className="btn btn-link" style={{"color": "var(--sm-green-dark"}}
                          href="/signup">Sign up</a>
                    </div>
                  {/* </Navbar.Text> */}
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
    }
  }

export default NavBar;