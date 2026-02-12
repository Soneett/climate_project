import React from "react";
import NavBar from "../../components/NavBar/NavBar";

export default function Layout({ children, navBarProps = {} }) {
  return (
    <>
      <NavBar {...navBarProps} />
      {children}
    </>
  );
}
