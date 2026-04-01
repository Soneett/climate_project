import React from "react";
import PropTypes from "prop-types";
import styles from "./IndicatorButton.module.scss";

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
