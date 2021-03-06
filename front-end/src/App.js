import './App.css';
import { Depart, Insert, Query, Log, Delete } from './components';

const nodes = [
  '127.0.0.1:5000',
  '127.1.0.0:4000',
  '255.255.255.1:8000'
];

function App() {
  return (
    <div className='App'>
      <Depart nodes={nodes}/>
      <Insert nodes={nodes}/>
      <Query nodes={nodes}/>
      <Log nodes={nodes}/>
      <Delete nodes={nodes}/>
    </div>
  );
}

export default App;
