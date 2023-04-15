import React from "react";
import icon from "../assets/images/icon.png";
import { Typography } from "@mui/material";

const Header = ({ title }) => {
  return (
    <div class="header">
      <img src={icon} />
      <Typography variant="h1" id="main-heading">
        {title}
      </Typography>
    </div>
  );
};

export default Header;
