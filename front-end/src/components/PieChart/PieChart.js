import React from 'react';
import Plot from 'react-plotly.js';

const PieChart = (props) => {
  const nodes = props.nodes.map(n => `${n.me.ip}:${n.me.port}`);
  const values = [1, 2, 3];

  return (
    <div className='mt-4'>
      <h2 className='text-center'>Key distribution</h2>
      <Plot
        data={[
        {
          type: 'pie',
          values: values,
          labels: nodes},
        ]}
        layout= {{
            width: 500,
            height: 500,
            paper_bgcolor:"#FFF0",
        }}
      />
    </div>
)};

export default PieChart;
