import React from 'react';

class Insert extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      key: '',
      value: '',
      node: props.nodes[0]
    };

    this.onKeyChange = this.onKeyChange.bind(this);
    this.onValueChange = this.onValueChange.bind(this);
    this.onNodeChange = this.onNodeChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  onKeyChange(event) {
    this.setState({key: event.target.value});
  }

  onValueChange(event) {
    this.setState({value: event.target.value});
  }

  onNodeChange(event) {
    this.setState({node: event.target.value});
  }

  handleSubmit(event) {
    console.log(this.state);
    alert('Inserting key, value...');
    event.preventDefault();
  }



  render() {
    return (
      <div>
        <h1>Insert</h1>
        <form onSubmit={this.handleSubmit}>
          <label>
            Key:
            <input type="text" value={this.state.key} onChange={this.onKeyChange} />
            Value:
            <input type="text" value={this.state.value} onChange={this.onValueChange} />
            Node:
            <select value={this.state.node} onChange={this.onNodeChange}>

            {this.props.nodes.map(node => (
              <option key={node} value={node}>
                {node}
              </option>
            ))}

            </select>
          </label>
          <input type="submit" value="Insert" />
        </form>
      </div>
    );
  }

}
export default Insert;
