import React from "react";
import styles from "./BlockHeader.module.scss";

const BlockHeader = ({ title }) => {
  return (
    <div className={styles.header}>
      <h3 className={styles.title}>{title}</h3>
    </div>
  );
};

export default BlockHeader;
