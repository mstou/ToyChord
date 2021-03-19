import React from 'react';
import { base_url } from '../constants';

class Query extends React.Component {
  constructor(props) {
    super(props);
    this.nodes = props.nodes.map(n => `${n.me.ip}:${n.me.port}`);

    this.state = {
      key: '',
      node: base_url,
      value: '',
      printAll: false,
      files: []
    };

    this.onKeyChange = this.onKeyChange.bind(this);
    this.onNodeChange = this.onNodeChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleClear = this.handleClear.bind(this);
  }

  onKeyChange(event) {
    this.setState({key: event.target.value});
  }

  onNodeChange(event) {
    this.setState({
      node: event.target.value,
      value: '',
      files: [],
      printAll: false
    });
  }

  handleClear(event) {
      this.setState({
        value: '',
        printAll: false,
        files: []
      })
  }

  handleSubmit(event) {
    const url = `http://${this.state.node}/query?key=${this.state.key}`;
    if (this.state.key === '*') {
      fetch(url)
      .then(res => res.json())
      .then(data => {
        const nodes = data.map(n => n.files);
        const files = nodes.map(n => {
          const vals = Object.values(n)
          return vals;
        })

        console.log(files);
        this.setState({
          value: '',
          files: files,
          printAll: true
        })})
      .catch(exc => console.log(exc))
    }
    else {
      fetch(url)
      .then(res => res.json())
      .then(data => {
        this.setState({
          value: data.value,
          printAll: false,
          files: []
        })})
      .catch(exc => console.log(exc))
    }

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
        {
          this.state.printAll
          ?
          <div>
            {this.state.files.map((file, ind) => (
              <div key={ind}>
                <p> <b>Node {ind}</b> </p>
                {
                  file.length
                  ?
                  file.map(f =>
                    <p key={f.name}>
                      Key: {f.name}<br/>
                      Value: {f.value}
                    </p>
                  )
                  :
                  <p> No files </p>
                }
              </div>
            ))}
            <button className="btn btn-primary" onClick={this.handleClear}>
              Clear
            </button>
            </div>
          :
          <p> </p>
        }
      </div>
    );
  }

}
export default Query;
