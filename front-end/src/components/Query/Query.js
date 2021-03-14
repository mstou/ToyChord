import React from 'react';

class Query extends React.Component {
  constructor(props) {
    super(props);
    this.nodes = props.nodes.map(n => `${n.me.ip}:${n.me.port}`);

    this.state = {
      key: '',
      node: this.nodes[0],
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
      value: ''
    });
  }

  handleSubmit(event) {
    console.log(this.state.key);
    // query request to server...
    const val = 'this is a test';
    this.setState({
      value: val
    });
    event.preventDefault();
  }

  render() {
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
              {this.nodes.map(node => (
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
          <p> </p>
        }
      </div>
    );
  }

}
export default Query;
