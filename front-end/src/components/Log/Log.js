import React from 'react';
import Node from './LogNode';
import { base_url } from '../constants';

class Log extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      selectedNode: base_url,
      index: 0,
      log: false,
    }

    this.handleChange = this.handleChange.bind(this);
    this.handleClear = this.handleClear.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    const node = event.target.value;
    const [ip, port] = node.split(':');
    const index = this.props.nodes.findIndex(n => (
      n.me.ip === ip && n.me.port === port
    ));

    this.setState({
      selectedNode: event.target.value,
      index: index
    });
  }

  handleClear(event) {
      this.setState({log: false});
  }

  handleSubmit(event) {
    console.log(this.state.selectedNode)
    this.setState({
      log: true
    })
    event.preventDefault();
  }

  render() {
    const nodes = this.props.nodes.map(n => `${n.me.ip}:${n.me.port}`);
    return (
      <div className='p-3'>
        <h2>Log</h2>
        <form onSubmit={this.handleSubmit}>
          <div className='form-group'>
            <label>Select node</label>
            <br/>
            <select value={this.state.selectedNode} onChange={this.handleChange}>
            {nodes.map((node, index) => (
              <option key={node} value={node}>
                {node}
              </option>
            ))}
            </select>
          </div>

          <input className="btn btn-primary" type="submit" value="Log" />
        </form>
        {
          this.state.log
          ?
          <div>
            <Node node={this.props.nodes[this.state.index]}/>
            <button className="btn btn-primary" onClick={this.handleClear}>
              Clear
            </button>
          </div>
          :
          <p> </p>

        }
      </div>
    )}
}

export default Log;
