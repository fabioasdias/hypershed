import * as React from "react";
import * as ReactDOM from "react-dom"
import * as d3_scale from "d3-scale";
import * as d3_axis from "d3-axis";
import * as d3_array from "d3-array";
import * as d3_selection from "d3-selection";

interface AxisProps {
  axisMargin: number,
  height: number,
  topMargin: number,
  data: number[]
}


export class AxisLeft extends React.Component<AxisProps, {}>{
  yScale: any;
  axis: any;
  constructor(props) {
    super();
    this.yScale = d3_scale.scaleLinear();
    this.axis = d3_axis.axisLeft()
      .scale(this.yScale)
      .tickFormat((d) => "n" + d);

    this.update_d3(props);
  }
  componentWillReceiveProps(newProps) {
    this.update_d3(newProps);
  }
  update_d3(props) {
    let extent = [d3_array.min(props.data.map(d => { return d3_array.min(d.children) } )),
      d3_array.max(props.data.map(d => { return d3_array.max(d.children) } ))];

    this.yScale
      .domain(extent)
      .range([props.height, 0]);
    this.axis
      .ticks(extent[1]-extent[0]);
  }

  componentDidUpdate() { this.renderAxis(); }
  componentDidMount() { this.renderAxis(); }
  renderAxis() {
    let node = ReactDOM.findDOMNode(this);
    d3_selection.select(node).call(this.axis);
  }

  render() {
    console.log("render left axis");
    let translate = `translate(${this.props.axisMargin-30}, ${this.props.axisMargin})`;
    return (
      <g className="axis" transform={translate}>
      </g>
    );
  }
}


export class AxisTop extends React.Component<AxisProps, {}>{
  xScale: any;
  axis: any;
  constructor(props) {
    super();
    this.xScale = d3_scale.scalePoint();
    this.axis = d3_axis.axisTop()
      .scale(this.xScale)
      .tickFormat((d) => "h" + d);

    this.update_d3(props);
  }
  componentWillReceiveProps(newProps) {
    this.update_d3(newProps);
  }
  update_d3(props) {
    let extent = [1, props.data.length];
    this.xScale
      .padding([0.1])
      .domain(d3_array.range(0, props.data.length))
      .range([0, props.width]);
    this.axis
      .ticks(extent[1]-extent[0]);
  }

  componentDidUpdate() { this.renderAxis(); }
  componentDidMount() { this.renderAxis(); }
  renderAxis() {
    let node = ReactDOM.findDOMNode(this);
    d3_selection.select(node).call(this.axis);
  }

  render() {
    console.log("render axis");
    let translate = `translate(${this.props.axisMargin}, ${this.props.axisMargin-15})`;
    return (
      <g className="axis" transform={translate}>
      </g>
    );
  }
}

// export default AxisLeft, AxisTop;
