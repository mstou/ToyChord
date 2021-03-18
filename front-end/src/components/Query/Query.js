import React from 'react';
import { base_url } from '../constants';

class Query extends React.Component {
  constructor(props) {
    super(props);
    this.nodes = props.nodes.map(n => `${n.me.ip}:${n.me.port}`);

    this.state = {
      key: '',
      node: base_url,
      value: ''
    };

    this.onKeyChange = this.onKeyChange.bind(this);
    this.onNodeChange = this.onNodeChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  onKeyChange(event) {
    this.setState({key: event.target.value});
  }

  onNodeChange(event) {
    this.setState({
      node: event.target.value,
      value: '',

    });
  }

  handleSubmit(event) {
    const url = `http://${this.state.node}/query?key=${this.state.key}`;

    fetch(url)
    .then(res => res.json())
    .then(data => (
      this.setState({
        value: data.value
      })))
    .catch(exc => console.log(exc))

    event.preventDefault();
  }

  render() {
    const nodes = this.props.nodes.map(n => `${n.me.ip}:${n.me.port}`);
    return (
      <div className='p-3'>
        <h2>Query</h2>
        <form onSubmit={this.handleSubmit}>
          <div className='form-group'>
            <label>Key</label>
            <br/>
            <input type="text" value={this.state.key} onChange={this.onKeyChange} />
            <br/>
            <label>Node</label>
            <br/>
            <select value={this.state.node} onChange={this.onNodeChange}>
              {nodes.map(node => (
                <option key={node} value={node}>
                  {node}
                </option>
              ))}
            </select>
          </div>
          <input className='btn btn-primary' type="submit" value="Query" />
        </form>
        {
          this.state.value
          ?
          <p className='mt-3'> Value: {this.state.value} </p>
          :
          <p>  </p>
        }
      </div>
    );
  }

}
export default Query;
