import React from 'react';
import './App.css';

interface IAppProps {}

interface IAppState {
  message: string
}

class App extends React.Component<IAppProps, IAppState> {
  constructor(props: IAppProps) {
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
      <div className="App">
      <h1>{this.state.message}</h1>
      </div>
    )
  }
}

export default App;
