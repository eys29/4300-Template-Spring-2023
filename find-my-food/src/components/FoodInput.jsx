import React from "react";
import Typography from "@mui/material/Typography";
import { TextField } from "@mui/material";
import foodIcon from "../assets/images/mag.png";

function sendFocus() {
  document.getElementById("filter-text-val").focus();
}

const FoodInput = ({}) => {
  return (
    <div class="input-box-searches">
      <div class="searches">
        <Typography variant="h2">Food</Typography>
        <div class="input-box" id="input-food" onclick={sendFocus}>
          <img src={foodIcon} />
          <TextField
            label="Search for a food"
            variant="outlined"
            id="filter-text-val"
          />
        </div>
      </div>
    </div>
  );
};

export default FoodInput;
