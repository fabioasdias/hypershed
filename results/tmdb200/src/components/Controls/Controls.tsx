import * as React from "react";

import './style.less';

interface ControlsProps {
  reorder: any;
}

export class Controls extends React.Component<ControlsProps, {}>{
  label: string;
  constructor(props: ControlsProps){
    super();
    this.label = "Order Groups"
  }

  handleClick = ()=>{
    this.props.reorder();
  }

  render() {
    let className = "btn btn-default";
    return (
      <div className="controls">
      <button className={className} onClick={this.handleClick}>
        {this.label}
      </button>
      </div>
    );
  }
}