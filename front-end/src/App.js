import './App.css';
import React from 'react';
import { Depart, Insert, Query, Log, Delete, Topology, PieChart } from './components';
import nodes from './input.js';

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

class App extends React.Component {
  constructor(props) {
    super(props);

    this.handleReload = this.handleReload.bind(this);
  }

  handleReload(event) {
    alert("reload")
  }

  render() {
    return (
      <div className='app container-fluid w-100 d-inline-block light-gray'>
        <h1 className='text-center mt-4 p-3'>ToyChord</h1>
        <div className='p-4'>
          <div className='row'>
            <div className='col'>
              <RightHalf nodes={nodes} handleReload={this.handleReload}/>
            </div>
            <div className='col'>
              <LeftHalf nodes={nodes}/>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

// function App() {
//     return (
//       <div>
//         <Delete nodes={nodes} />
//         <Depart nodes={nodes} />
//         <Insert nodes={nodes} />
//         <Log nodes={nodes} />
//         <Query nodes={nodes} />
//         <PieChart nodes={nodes} />
//         <Topology nodes={nodes} />
//       </div>
//     )
// }

export default App;
