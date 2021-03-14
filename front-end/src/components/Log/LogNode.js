import React from 'react';

const zip = (a, b) => a.map((k, i) => [k, b[i]]);

const Node = ({node}) => {
  const fileKeys = Object.keys(node.files);
  const fileValues = Object.values(node.files).map(v => v.value);
  const files = zip(fileKeys, fileValues);

  const replicas = node.replicas.map(r => {
    const [key] = Object.keys(r);
    const val = r[key].value;
    return {key, val};
  })


  return (
    <div>
      <p> <b>Files</b>: </p>
      {files.map(f => (
        <div key={f[0]}>
          <p> Key: {f[0].substring(30, 40)} </p>
          <p> Value: {f[1]} </p>
        </div>
      ))}
      <p> <b>Replicas</b>: </p>
      {replicas.map(r => (
        <div key={r.key}>
          <p> Key: {r.key.substring(30, 40)} </p>
          <p> Value: {r.val} </p>
        </div>
      ))}

    </div>
)};

export default Node;
