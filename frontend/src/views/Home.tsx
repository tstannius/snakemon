import React, { CSSProperties } from 'react';

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
    const style = {
      marginLeft: "auto",
      marginRight: "auto",
  } as CSSProperties;

    return (
      <div className="centered">
        <h1>{this.state.message}</h1>
      </div>
    )
  }
}

export default Home;
