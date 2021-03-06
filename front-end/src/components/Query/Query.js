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
      <div>
        <h1>Query</h1>
        <form onSubmit={this.handleSubmit}>
          <label>
            Key:
            <input type="text" value={this.state.key} onChange={this.onKeyChange} />
            Node:
            <select value={this.state.node} onChange={this.onNodeChange}>

            {this.props.nodes.map(node => (
              <option key={node} value={node}>
                {node}
              </option>
            ))}

            </select>
          </label>
          <input type="submit" value="Query" />
        </form>
      </div>
    );
  }

}
export default Query;
