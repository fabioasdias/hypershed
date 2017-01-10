import * as React from "react";
import * as d3_request from "d3-request";

import {HyperlinkChart} from "../HyperlinkChart/HyperlinkChart";

import {Controls} from "../Controls/Controls";


export interface VisProps { urlNodes: string, urlLinks: string}
export interface VisState { links: any[], nodes: any[]}
export interface Margin { topMargin: number, leftMargin: number, rightMargin: number, bottomMargin: number }

export class Vis extends React.Component<VisProps, {}> {
  state: VisState;
  margin: Margin;
  width: number;
  height: number;
  linkOrder: number;

  constructor() {
    super();

    this.margin = {topMargin: 20,leftMargin: 4, rightMargin: 20, bottomMargin: 20};

    this.linkOrder = 0;
    this.state = {
      links: [],
      nodes: []
    };
  }
  componentWillMount() {
    this.loadRawData();
  }
  loadRawData() {
    d3_request.json(this.props.urlNodes)
      .get((error, data_nodes) => {
        if (error) {
          console.error(error);
          console.error(error.stack);
        }else{
          d3_request.json(this.props.urlLinks)
            .get((error, data_links) => {
              if (error) {
                console.error(error);
                console.error(error.stack);
              } else {

                let nodes = data_nodes.nodes;
                let links = data_links.links;

                links.forEach(function (d, i) {
                  d.id = i;
                  d.children = d.children.sort((a,b)=>{return a - b;});
                });

                this.width = links.length*15;
                this.height = nodes.length*15;

                this.setState({links: links, nodes: nodes});
              }});
        } });
  }

  reorderGroups = ()=>{
    this.linkOrder = 1;
    this.forceUpdate()
  }

  render() {
    if (this.state.links.length == 0) {
      return (
        <div>loading</div>
      );
    }
    return (
      <div>
        <Controls reorder={this.reorderGroups}/>
          <HyperlinkChart
            margin={this.margin}
            axisMargin={150}
            width={this.width}
            height={this.height}
            links={this.state.links}
            nodes={this.state.nodes}
            linkOrder={this.linkOrder}/>
      </div>
    );
  }
}

export default Vis;
