import * as React from "react";
import * as d3_scale from "d3-scale";
import * as d3_array from "d3-array"

import {AxisLeft} from './AxisLeft';
import {AxisTop} from './AxisTop';
import {HyperlinkView} from './HyperlinkView';
import {LinkHighlight} from './LinkHighlight';
import {NodeHighlight} from './NodeHighlight';

import './style.less';

export interface Margin {
  topMargin: number,
  leftMargin: number,
  rightMargin: number,
  bottomMargin: number
}

export interface HyperlinkChartProps {
  margin: Margin,
  axisMargin: number,
  width: number,
  height: number,
  links: any,
  nodes: any,
  linkOrder: number
}

export interface  HyperlinkChartState{
  linkHighlighted: number,
  nodeHighlighted: number
}

export class HyperlinkChart extends React.Component<HyperlinkChartProps, {}>{
  state: HyperlinkChartState;
  xScale: any;
  yScale: any;
  colorScale: any;
  nodeOrder: number[];
  linkOrder: number[];

  constructor(props: HyperlinkChartProps){
    super();
    this.xScale = d3_scale.scalePoint();
    this.yScale = d3_scale.scalePoint();
    this.colorScale = d3_scale.scaleOrdinal(d3_scale.schemeCategory20);
    this.update_d3(props);
  }
  componentWillReceiveProps(newProps: HyperlinkChartProps){
    this.update_d3(newProps);
  }



  private update_d3(props: HyperlinkChartProps) {
    this.state = {
      linkHighlighted: -1,
      nodeHighlighted: -1
    };

    this.linkOrder = this.getLinksOrder(props);
    this.nodeOrder = props.nodes.map(d => d.id);

    this.xScale
      .padding([0.1])
      .domain(this.linkOrder)
      .range([0, props.width]);
    this.yScale
      .domain(this.nodeOrder)
      .range([0, props.height]);

  }

  private getLinksOrder=(props)=>{
    if(props.linkOrder==0)
      return props.links.map(d => d.id);
    if(props.linkOrder==1)
      return this.orderGroups(props);
  }

  private orderGroups=(props)=>{
    let links = props.links.map((l) =>{ return {id: l.id, group: l.group}});
    links.sort((a,b) => {return a.group - b.group});
    return links.map(l => l.id);
  }

  private getLink = (l)=>{
    return this.props.links[l];
  }

  private reorderNodes = (newOrder)=>{
    this.nodeOrder = newOrder;
    this.yScale.domain(this.nodeOrder);
  }

  private reorderLinks = (newOrder)=>{
    this.linkOrder = newOrder;
    this.xScale.domain(this.linkOrder);
  }
  private getNodes=(l)=>{
    let link = this.getLink(l);
    return link.children;
  };

  private getLinks = (n)=>{
    let links = this.props.links.filter((l)=>{
      return l.children.indexOf(n)>=0;
    });
    return links;
  }

  private linkBasedOrder = (l)=>{
    let children = this.getNodes(l);
    let newOrder = children;
    let prev = 0;
    children.forEach((n)=>{
      newOrder = newOrder.concat(d3_array.range(prev, n));
      prev = n+1;
    })
    newOrder = newOrder.concat(d3_array.range(prev, this.props.nodes.length));

    this.reorderNodes(newOrder);
  }
  private nodeBasedOrder = (n)=>{

    let links = this.getLinks(n).map((l) => l.id);
    let newOrder = links;
    let prev = 0;
    links.forEach((l)=>{
      newOrder = newOrder.concat(d3_array.range(prev, l));
      prev = l+1;
    })
    newOrder = newOrder.concat(d3_array.range(prev, this.props.links.length));
    this.reorderLinks(newOrder);
  }

  linkLabelClicked = (l)=>{

    this.linkBasedOrder(l);

    console.log("link clicked", l);
    this.setState({
      linkHighlighted: l
    })
  }

  nodeHover = (l, n)=>{
    console.log("node hover", l, n);
    this.setState({
      nodeHighlighted: n,
      linkHighlighted: l
    })
  }

  nodeLabelClicked = (n)=>{
    this.nodeBasedOrder(n);
    this.setState({
      nodeHighlighted: n
    })
  }


  render(){
    console.log('HyperlinkChart >>>> render', this.state);
    let translate = `translate(${this.props.margin.leftMargin}, ${this.props.margin.topMargin} )`;
    return (
    <svg width={this.props.width + this.props.axisMargin +  this.props.margin.leftMargin +  this.props.margin.rightMargin}
    height={this.props.height + this.props.axisMargin +  this.props.margin.topMargin + this.props.margin.bottomMargin}>
        <g className="linkChart" transform={translate}>
          <g>
            <LinkHighlight  xScale={this.xScale}
                            height={this.props.height}
                            axisMargin={this.props.axisMargin}
                            id={this.state.linkHighlighted}/>
            <NodeHighlight  yScale={this.yScale}
                            width={this.props.width}
                            axisMargin={this.props.axisMargin}
                            id={this.state.nodeHighlighted}/>
          </g>
        <g>
          <AxisTop xScale={this.xScale}
                   axisMargin={this.props.axisMargin}
                   data={this.props.links}
                   label={0}
                   labelClicked={this.linkLabelClicked}/>
          <AxisLeft yScale={this.yScale}
                    axisMargin={this.props.axisMargin}
                    data={this.props.nodes}
                    label={0} labelClicked={this.nodeLabelClicked}/>
          <HyperlinkView xScale={this.xScale} yScale={this.yScale}
                         colorScale={this.colorScale}
                         axisMargin={this.props.axisMargin}
                         height={this.props.height}
                         links={this.props.links}
                         nodeHover={this.nodeHover}/>
        </g>

        </g>
    </svg>
    );
  }
}


export default HyperlinkChart;
