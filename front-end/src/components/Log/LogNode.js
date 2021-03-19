import React from 'react';

const Node = ({node}) => {
  const files = Object.values(node.files).map(f => ({
    key: f.name,
    value: f.value
  }));

  const replicas = node.replicas.map((r, ind) => {
    const keys = Object.keys(r);
    if (keys.length) {
      const f = keys.map(k => ({
        key: r[k].name,
        value: r[k].value
      }));
      return f;
    }
    else {
      return [];
    }
  })

  return (
    <div className='mt-2'>
      <p><b>Files</b>:</p>
      { files.length
        ?
          files.map(f => (
            <div key={f.key}>
              <p>
                Key: {f.key} <br/>
                Value: {f.value}
              </p>
            </div>
          ))
        :
        <p> No files </p>
      }
      <p><b>Replicas</b>:</p>
      {replicas.map((replica, ind) => (
        <div key={ind}>
          <p> <b>replica {ind}</b> </p>
          { replica.length
            ?
              replica.map(r =>
                <p key={r.key}>
                  Key: {r.key}<br/>
                  Value: {r.value}
                </p>
              )

            :
            <p> No replicas </p>
          }
        </div>
      ))}
    </div>
)};

export default Node;
