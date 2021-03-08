import React from 'react';

class Log extends React.Component {
  constructor(props) {
    super(props);
    this.state = {selectedNode: props.nodes[0] || null }

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({selectedNode: event.target.value});
  }

  handleSubmit(event) {
    console.log(this.state.selectedNode)
    alert(`Node logged: ${this.state.selectedNode}`);
    event.preventDefault();
  }

  render() {
    return this.state.selectedNode ?
      (<div className='p-3'>
        <h2>Log</h2>
        <form onSubmit={this.handleSubmit}>
          <div className='form-group'>
            <label>Select node</label>
            <br/>
            <select value={this.state.value} onChange={this.handleChange}>
            {this.props.nodes.map(node => (
              <option key={node} value={node}>
                {node}
              </option>
            ))}
            </select>
          </div>

          <input className="btn btn-primary" type="submit" value="Log" />
        </form>
      </div>)
      :
      <p>No nodes in ToyChord...</p>

  }
}

export default Log;
