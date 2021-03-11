import './App.css';
import { Depart, Insert, Query, Log, Delete, Topology, PieChart } from './components';

const nodes = [
  '127.0.0.1:5000',
  '127.1.0.0:4000',
  '255.255.255.1:8000'
];

const LeftHalf = () => (
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

const RightHalf = () => (
  <>
    <div className='row'>
      <Topology />
    </div>
    <div className='row mt-5'>
      <PieChart />
    </div>
  </>
);

function App() {
  return (
    <div className='app container-fluid w-100 d-inline-block light-gray'>
      <h1 className='text-center mt-4 p-3'>ToyChord</h1>
      <div className='p-4'>
        <div className='row'>
          <div className='col'>
            <RightHalf />
          </div>
          <div className='col'>
            <LeftHalf />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
