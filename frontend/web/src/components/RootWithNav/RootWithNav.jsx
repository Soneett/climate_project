import React, { useState } from "react";
import NavBar from "../NavBar/NavBar";
import HomePage from "../HomePage/HomePage";


const RootWithNav = () => {
  return (
    <div>
      <NavBar />
      <HomePage />
    </div>
  );
}

export default RootWithNav