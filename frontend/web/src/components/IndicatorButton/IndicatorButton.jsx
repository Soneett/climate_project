import React from "react";
import styles from "./IndicatorButton.module.scss";

const IndicatorButton = ({ 
  label, 
  state = "default", // "default", "selected", "disabled"
  onClick = () => {},
  size = "medium" // "medium" or "small"
}) => {
  const handleClick = () => {
    if (state !== "disabled") {
      onClick();
    }
  };

  return (
    <button
      type="button"
      className={`${styles.button} ${styles[state]} ${styles[size]}`}
      onClick={handleClick}
      disabled={state === "disabled"}
    >
      {label}
    </button>
  );
};

export default IndicatorButton;
