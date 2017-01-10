import * as React from "react";

interface AxisProps {
  yScale: any,
  axisMargin: number,
  data: any[],
  labelClicked: any
}

export class AxisLeft extends React.Component<AxisProps, {}>{
  data: any[];
  constructor(props) {
    super();
    this.update_d3(props);
  }
  componentWillReceiveProps(newProps) {
    this.update_d3(newProps);
  }

  update_d3(props) {
    //TODO: this should take into account nodesOrder
    this.data = props.data.map((d) => { return {y: props.yScale(d.id), id: d.id, d: d.name}});
  }

  handleClick(l) {
    this.props.labelClicked(l.id);
  }

  renderLabel = (l: any, i: number) => {
    let key = "node-label-"+ i;
    let translate = "translate(0, " + l.y+ ")"
    let rotate = "";//"rotate(60)";
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
    console.log('AxisLeft >>>> render');
    let translate = `translate(${this.props.axisMargin-20}, ${this.props.axisMargin})`;
    return (
      <g className="labels nodes" transform={translate}>
        {this.data.map(this.renderLabel)}
      </g>
    );
  }
}

// export default AxisLeft, AxisTop;
