import React from "react";
import PropTypes from "prop-types";
import styles from "./BlockHeader.module.scss";

const BlockHeader = ({ title }) => {
  return (
    <div className={styles.header}>
      <h3 className={styles.title}>{title}</h3>
    </div>
  );
};

BlockHeader.propTypes = {
  title: PropTypes.string.isRequired
};

export default React.memo(BlockHeader);
