import * as React from "react";
import * as d3_scale from "d3-scale";
import * as d3_array from "d3-array";

interface NodeHighlightProps {
  yScale: any,
  axisMargin: number,
  width: number,
  id: any
}

export class NodeHighlight extends React.Component<NodeHighlightProps, {}>{
  data: any;
  constructor(props) {
    super();
    this.update_d3(props);
  }
  componentWillReceiveProps(newProps) {
    this.update_d3(newProps);
  }

  update_d3(props) {
    if(props.id == -1){
      this.data = {};
      return;
    }
    var height = Math.min(props.yScale.step(), 15);
    this.data = {y: props.yScale(props.id)-.75*height, width: props.width+2*height, height: height};

  }

  render() {
    console.log('NodeHighlight >>>> render');

    if(Object.keys(this.data).length === 0) return null;

    let translate = `translate(${this.props.axisMargin-10}, ${this.props.axisMargin})`;
    return (
      <g  transform={translate}>
       <rect className="nodeHighlight"  width={this.data.width} height={this.data.height} y={this.data.y} ></rect>
      </g>
    );
  }
}

// export default AxisLeft, AxisTop;
