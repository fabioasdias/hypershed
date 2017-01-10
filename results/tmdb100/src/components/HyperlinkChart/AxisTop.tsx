import * as React from "react";
import * as d3_array from "d3-array";

interface AxisProps {
  xScale: any,
  axisMargin: number,
  data: any[],
  labelClicked: any
}

export class AxisTop extends React.Component<AxisProps, {}>{
  data: any[];
  constructor(props) {
    super();
    this.update_d3(props);
  }
  componentWillReceiveProps(newProps) {
    this.update_d3(newProps);
  }

  update_d3(props) {
    this.data = props.data.map((d) => { return {x: props.xScale(d.id), id: d.id, d: d.name}});
  }

  handleClick(l) {
    this.props.labelClicked(l.id);
  }

  renderLabel = (l: any) => {
    let key = "label-"+ l.id;
    let translate = "translate(" + l.x+ ",0)"
    let rotate = "rotate(60)";
    return (
      <text textAnchor="end" className="label"
            key={key}
            onClick={() => this.handleClick(l)}
            transform={translate+rotate}>
        {l.d}
      </text>
    )
      ;
  }
  render() {
    console.log('AxisTop >>>> render');
    let translate = `translate(${this.props.axisMargin}, ${this.props.axisMargin-20})`;
    return (
      <g className="labels" transform={translate}>
        {this.data.map(this.renderLabel)}
      </g>
    );
  }
}

// export default AxisLeft, AxisTop;
