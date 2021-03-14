import React from 'react';

const Node = ({node}) => {
  const files = Object.values(node.files).map(f => ({
    key: f.name, 
    value: f.value
  }));

  const replicas = node.replicas.map(r => {
    const [k] = Object.keys(r);
    const key = r[k].name;
    const value = r[k].value;
    return {key, value};
  })


  return (
    <div className='mt-2'>
      <p><b>Files</b>:</p>
      {files.map(f => (
        <div key={f.key}>
          <p>
            Key: {f.key} <br/>
            Value: {f.value}
          </p>
        </div>
      ))}
      <p><b>Replicas</b>:</p>
      {replicas.map(r => (
        <div key={r.key}>
          <p>
            Key: {r.key}<br/>
            Value: {r.value}
          </p>
        </div>
      ))}
    </div>
)};

export default Node;
