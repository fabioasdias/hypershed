import * as React from "react";
import * as d3_scale from "d3-scale";
import * as d3_array from "d3-array";

interface LinkHighlightProps {
  xScale: any,
  axisMargin: number,
  height: number,
  id: any
}

export class LinkHighlight extends React.Component<LinkHighlightProps, {}>{
  xScale: any;
  data: any;
  constructor(props) {
    super();
    this.xScale = d3_scale.scalePoint();
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

    var width = Math.min(props.xScale.step(), 30);
    this.data = {x: props.xScale(props.id)-width/2, height: props.height+1.5*width, width: width};
  }

  render() {
    console.log('LinkHighlight >>>> render');
    if(Object.keys(this.data).length === 0) return null;
    let translate = `translate(${this.props.axisMargin}, ${this.props.axisMargin-this.data.width})`;
    return (
      <g  transform={translate}>
       <rect className="linkHighlight"  width={this.data.width} height={this.data.height} x={this.data.x} ></rect>
      </g>
    );
  }
}

// export default AxisLeft, AxisTop;
