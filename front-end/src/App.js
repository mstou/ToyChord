import './App.css';
import React from 'react';
import { Depart, Insert, Query, Log, Delete, Topology, PieChart, Info } from './components';
import { base_url } from './components/constants';

const LeftHalf = ({nodes}) => (
  <>
    <div className='row pt-3'>
      <div className='col'>
        <Log nodes={nodes}/>
      </div>
      <div className='col'>
        <Depart nodes={nodes}/>
      </div>
    </div>
    <div className='row pt-3'>
      <div className='col'>
        <Query nodes={nodes}/>
      </div>
      <div className='col'>
        <Delete nodes={nodes}/>
      </div>
    </div>
    <div className='row pt-3'>
      <div className='col'>
        <Insert nodes={nodes}/>
      </div>
      <div className='col'>
        <Info K={5} consistency={'Linearizability'}/>
      </div>
    </div>
  </>
);

const RightHalf = ({nodes, handleReload}) => (
  <>
    <div className='row'>
      <Topology nodes={nodes} handleReload={handleReload}/>
    </div>
    <div className='row mt-5'>
      <PieChart nodes={nodes}/>
    </div>
  </>
);

const fetchNodes = async () => {
  const bootstrap = base_url;
  let next = bootstrap; // start from bootstrap node
  const nodes = [];

  let cnt = 0; // safety counter
  while (true) {
    const url = `http://${next}/log`;
    const res = await fetch(url);
    const node = await res.json();
    nodes.push(node);

    next = `${node.next.ip}:${node.next.port}`;
    if (next === bootstrap || !nodes) {
      break;
    }

    cnt += 1;
    if (cnt > 10) {
      console.log("Too many nodes to handle...");
      break;
    }
  }
  return nodes;
}

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      nodes: []
    }
    this.handleReload = this.handleReload.bind(this);
  }

  async componentDidMount() {
    const nodes = await fetchNodes();
    this.setState({
      nodes: nodes
    });
  }

  async handleReload(event) {
    const nodes = await fetchNodes();
    this.setState({
      nodes: nodes
    });
  }

  render() {
    return (
      <div className='app container-fluid w-100 d-inline-block'>
        <h1 className='text-center mt-4 p-3'>ToyChord</h1>
        <div className='p-4'>
          <div className='row'>
            <div className='col'>
              <RightHalf nodes={this.state.nodes} handleReload={this.handleReload}/>
            </div>
            <div className='col'>
              <LeftHalf nodes={this.state.nodes}/>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default App;
