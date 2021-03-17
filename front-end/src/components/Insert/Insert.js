import React from 'react';

class Insert extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      key: '',
      value: '',
      node: ''
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
    const nodes = this.props.nodes.map(n => `${n.me.ip}:${n.me.port}`);
    return (
      <div className='p-3'>
        <h2>Insert</h2>
        <form onSubmit={this.handleSubmit}>
          <div className='form-group'>
            <label>Key</label>
            <br/>
            <input type="text" value={this.state.key} onChange={this.onKeyChange} />
            <br/>
            <label>Value</label>
            <br/>
            <input type="text" value={this.state.value} onChange={this.onValueChange} />
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
            <br/>
          </div>
          <input className='btn btn-primary' type="submit" value="Insert" />
        </form>
      </div>
    );
  }

}
export default Insert;
