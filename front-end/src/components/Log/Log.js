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
      (<div>
        <h1>Log</h1>
        <form onSubmit={this.handleSubmit}>
          <label>
            Select node:
            <select value={this.state.value} onChange={this.handleChange}>

            {this.props.nodes.map(node => (
              <option key={node} value={node}>
                {node}
              </option>
            ))}

            </select>
          </label>
          <input type="submit" value="Log" />
        </form>
      </div>)
      :
      <p>No nodes in ToyChord...</p>

  }
}

export default Log;
