import React from 'react';

class Depart extends React.Component {
  constructor(props) {
    super(props);
    this.state = {selectedNode: ''};

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({selectedNode: event.target.value});
  }

  handleSubmit(event) {
    console.log(this.state.selectedNode)
    alert(`Node departed: ${this.state.selectedNode}`);
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
