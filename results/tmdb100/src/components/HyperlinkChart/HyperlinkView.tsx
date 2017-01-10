import * as React from "react";
import * as d3_array from "d3-array"


interface HyperlinksViewProps {
  yScale: any,
  xScale: any,
  colorScale: any,
  axisMargin: number,
  height: number,
  links: LinkData[],
  nodeHover: any
}
interface LinkData {
  children: number[],
  id: number,
  group: number,
  name: string
}

export class HyperlinkView extends React.Component<HyperlinksViewProps, {}> {
  radio: number;
  constructor(props) {
    super();
    this.update_d3(props);
  }
  componentWillReceiveProps(newProps) {
    this.update_d3(newProps);
  }

  update_d3(props) {
    this.radio = Math.min(props.xScale.step(), 15)/3;
  }

  makeLink = (d: LinkData) => {
    let linkProps: HyperlinkProps = {
      id: d.id,
      x: this.props.xScale(d.id),
      y: d.children.map(e => this.props.yScale(e)),
      nIds: d.children,
      radio: this.radio,
      color: this.props.colorScale(d.group),
      nodeHover: this.props.nodeHover
    };
    var key = "link-"+d.id;

    return (
      < HyperLink {...linkProps} key={key} />
    );
  }

  render(){
    let translateLinks = `translate(${this.props.axisMargin}, 
      ${this.props.axisMargin})`;
  return(
    <g className="links"  transform={translateLinks}>
      {this.props.links.map(this.makeLink)}
    </g>
  );
  }

}

interface HyperlinkProps {
  id: number,
  x: number,
  y: number[],
  nIds: number[],
  radio: number,
  color: string,
  nodeHover: any
}


export class HyperLink extends React.Component<HyperlinkProps, {}>{

  renderLink = () =>{

    let linkProps: LinkProps = {
      y1: d3_array.min(this.props.y),
      y2: d3_array.max(this.props.y),
      id: this.props.id,
      color: this.props.color
    };

    let key = "link-"+this.props.x;

    return(
      <Link {...linkProps} key={key}/>
    );
  }

  renderNode = (pos: any, i: number) => {
    let key = "node-"+this.props.id+"-"+i;

    let nodeProps: NodeProps = {
      x: 0,
      y: pos,
      id: this.props.nIds[i],
      radio: this.props.radio,
      color: this.props.color,
      nodeHover: (nId) => this.props.nodeHover(this.props.id, nId)
    };
    return (
      <Node {...nodeProps} key={key} />
        );
  }

  render(){
    let translate = `translate(${this.props.x} , 0 )`;
    return(
      <g transform={translate}>
        {this.renderLink()}
        {this.props.y.map(this.renderNode)}
      </g>
    );
  }

}


//

interface NodeProps {
  x: number,
  y: number,
  id: number,
  radio: number,
  color: string,
  nodeHover: any
}


export class Node extends React.Component<NodeProps, {}> {

  mouseOver = ()=>{
    this.props.nodeHover(this.props.id);
  }

  render(){
    return(
      <circle className="node"
              r={this.props.radio}
              fill={this.props.color}
              cx={this.props.x}
              cy={this.props.y-this.props.radio}
              onMouseOver={() => this.mouseOver()}
      />
    );
  }

}

//

interface LinkProps {
  y1: number,
  y2: number,
  id: number,
  color: string
}


export class Link extends React.Component<LinkProps, {}> {

  render(){
    return(
      <line className="link"
            stroke={this.props.color}
            y1={this.props.y1}
            y2={this.props.y2}
      />
    );
  }

}