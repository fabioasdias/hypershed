import * as React from "react";
import * as ReactDOM from "react-dom";

import {Vis} from "./components/HypergraphVis/index";

ReactDOM.render(
  <Vis urlNodes="data/tmdb100/l0.json"
       urlLinks="data/tmdb100/l0.json"/>,
    document.getElementById("app")
);

