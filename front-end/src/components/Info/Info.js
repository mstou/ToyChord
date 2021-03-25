import React from 'react';
import { base_url } from '../constants';

const Info = (props) => (
  <div className='p-3'>
    <h5><b>Number of replicas:</b> {props.K}</h5>
    <h5><b>Consistency:</b> {props.consistency}</h5>
  </div>
);

export default Info;
