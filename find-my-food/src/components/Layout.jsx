import React from "react";
import Header from "./Header";
import FoodInput from "./FoodInput";
import { Container, Typography } from "@mui/material";

const Layout = ({ children, title }) => {
  return (
    <body>
      <div class="full-body-container">
        <div class="top-text">
          <Header title={title}></Header>
          <FoodInput></FoodInput>
        </div>
      </div>
    </body>
  );
};

export default Layout;
