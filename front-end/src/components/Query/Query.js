import React from 'react';

class Query extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      key: '',
      node: props.nodes[0]
    };

    this.onKeyChange = this.onKeyChange.bind(this);
    this.onNodeChange = this.onNodeChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  onKeyChange(event) {
    this.setState({key: event.target.value});
  }

  onNodeChange(event) {
    this.setState({node: event.target.value});
  }

  handleSubmit(event) {
    console.log(this.state);
    alert('Querying key, node...');
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
              {this.props.nodes.map(node => (
                <option key={node} value={node}>
                  {node}
                </option>
              ))}
            </select>
          </div>
          <input className='btn btn-primary' type="submit" value="Query" />
        </form>
      </div>
    );
  }

}
export default Query;
