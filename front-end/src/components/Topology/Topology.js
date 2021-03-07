import React from 'react';
import Sketch from 'react-p5'

const [sizeX, sizeY] = [500, 500];
const [centerX, centerY] = [sizeX/2, sizeY/2];
const D = 400;
const d = 100;
const R = D / 2;
const r = d / 2;
const n = 7;
const theta = 2 * Math.PI / n;

function Topology() {
  const setup = (p5, canvasParentRef) => {
    p5.createCanvas(sizeX, sizeY).parent(canvasParentRef)
  }

  const draw = p5 => {
    p5.background(255, 130, 20)

    // draw network circle of radius R
    p5.circle(centerX, centerY, D)

    // draw node circles of radius r
    let angle = 0;
    for (let i=0; i<n; i++) {
      const x = centerX + R * Math.sin(angle);
      const y = centerY + R * Math.cos(angle);
      const text = '127.0.0.1:5000';
      p5.circle(x, y, d);
      p5.textAlign(p5.CENTER, p5.CENTER);
      p5.textSize(15);
      p5.text(text, x, y);
      angle = angle + theta;
    }
  }

  return <Sketch setup={setup} draw={draw} />
}

export default Topology;
