import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./App";
import { globalConfig, JokTheme } from "re-jok";

globalConfig();

ReactDOM.render(
  <React.StrictMode>
    <JokTheme>
      <App />
    </JokTheme>
  </React.StrictMode>,
  document.getElementById("root")
);
