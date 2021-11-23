import React from 'react';
import Container from 'react-bootstrap/Container'
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import { Routes, Route, Outlet, Link } from "react-router-dom";
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';


class Layout extends React.Component {
  render(): JSX.Element {
    return (
      <div>
        <Navbar bg="light">
          <Container>
            <Navbar.Brand href="/">SnakeMon</Navbar.Brand>
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


interface IWorkflowsProps {}
interface IWorkflowsState {}
class Workflows extends React.Component<IHomeProps, IHomeState> {
  render(): JSX.Element {
    const placeholder = "All of my workflows";
    return (
      <div>
        <h1>placeholder</h1>
      </div>
    )
  }
}


interface IHomeProps {}
interface IHomeState {
  message: string
}
class Home extends React.Component<IHomeProps, IHomeState> {
  constructor(props: IHomeProps) {
    super(props);
    this.state = {
      message: "Waiting on response from backend ...",
    };
  }

  componentDidMount() {
    fetch("http://localhost:8000/")
    .then(response => response.json())
    .then(data => {this.setState({message: data.message,})})
  }

  render(): JSX.Element {
    return (
      <div>
        <h1>{this.state.message}</h1>
      </div>
    )
  }
}


class App extends React.Component {
  render(): JSX.Element {
    return (
      <div className="App">
        <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} /> {/* note only home has index */}
          <Route path="workflows" element={<Workflows />} />

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
