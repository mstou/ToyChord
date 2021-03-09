import React from 'react';
import Plot from 'react-plotly.js';

const PieChart = (props) => {
  const values = [1, 2, 3];
  const labels = ['127.0.0.1:5000', '127.0.0.1:3000', '127.0.0.1:8000'];
  return (
    <div className='mt-4'>
      <h2 className='text-center'>Key distribution</h2>
      <Plot
        data={[
        {
          type: 'pie',
          values: values,
          labels: labels},
        ]}
        layout={ {width: 500, height: 500} }
      />
    </div>
)};

export default PieChart;
