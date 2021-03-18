import React from 'react';
import { base_url } from '../constants';

class Depart extends React.Component {
  constructor(props) {
    super(props);
    this.state = {selectedNode: base_url};

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({selectedNode: event.target.value});
  }

  handleSubmit(event) {
    const url = `http://${this.state.selectedNode}/depart`;
    if (this.state.selectedNode !== base_url) {
      fetch(url)
      .then(res => console.log(res))
      .catch(exc => console.log(exc))
    }
    else {
      console.log('Cannot depart bootstrap node.');
    }

    event.preventDefault();
  }

  render() {
    const nodes = this.props.nodes.map(n => `${n.me.ip}:${n.me.port}`);
    return (
      <div className='p-3'>
        <h2>Depart</h2>
        <form onSubmit={this.handleSubmit}>
          <div className='form-group'>
            <label>Select node</label>
            <br/>
            <select value={this.state.value} onChange={this.handleChange}>
            {nodes.map(node => (
              <option key={node} value={node}>
                {node}
              </option>
            ))}
            </select>
          </div>
          <input className='btn btn-primary' type="submit" value="Depart" />
        </form>
      </div>
    )}
}

export default Depart;
