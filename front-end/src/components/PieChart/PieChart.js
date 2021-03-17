import React from 'react';
import Plot from 'react-plotly.js';
import BigInt from 'big-integer';

const PieChart = (props) => {
  let nodes = [];
  let labels = [];
  let values = [];
  let percentages = [];

  if (props.nodes.length) {
    nodes = props.nodes.map(n => ({
      id: BigInt(n.me.id, 16),
      label: `${n.me.ip}:${n.me.port}`
    }));
    nodes = nodes.sort((a, b) => a.id - b.id);
    labels = nodes.map(n => n.label);
    const total = BigInt('10000000000000000000000000000000000000000', 16);
    values = nodes.map(n => n.id);
    percentages = [];
    percentages.push((values[0] + total - values[values.length-1])/ total);
    for (let i=1; i<values.length; i++) {
      percentages.push((values[i] - values[i-1])/total);
    }
  }

  return (
    <div className='mt-4'>
      <h2 className='text-center'>Key distribution</h2>
      <Plot
        data={[
        {
          type: 'pie',
          values: percentages,
          labels: labels},
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
