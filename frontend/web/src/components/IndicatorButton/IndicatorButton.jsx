import React from "react";
import PropTypes from "prop-types";
import styles from "./IndicatorButton.module.scss";

/**
 * IndicatorButton component
 * Displays a button with different visual states
 * @param {string} label - Button text
 * @param {string} state - Button state: "default", "selected", or "disabled"
 * @param {Function} onClick - Click handler
 * @param {string} size - Button size: "medium" or "small"
 */
const IndicatorButton = ({ 
  label, 
  state = "default",
  onClick = () => {},
  size = "medium"
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

IndicatorButton.propTypes = {
  label: PropTypes.string.isRequired,
  state: PropTypes.oneOf(["default", "selected", "disabled"]),
  onClick: PropTypes.func,
  size: PropTypes.oneOf(["medium", "small"])
};

export default React.memo(IndicatorButton);
