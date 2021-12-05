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
            <Container>
              <Navbar.Brand href="/">
              <Logo />{' '}
                SnakeMon</Navbar.Brand>
              <Navbar.Toggle aria-controls="basic-navbar-nav" />
              <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="me-auto">
                  <Nav.Link href="/workflows">Workflows</Nav.Link>
                </Nav>
              </Navbar.Collapse>
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