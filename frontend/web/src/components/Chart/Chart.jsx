import React from "react";
import styles from "./Chart.module.scss";

const Chart = ({ type = "bar" }) => {
  return (
    <div className={styles.chart}>
      <div className={styles.placeholder}>
        <p className={styles.text}>График ({type})</p>
        <p className={styles.subtext}>Данные загружаются...</p>
      </div>
    </div>
  );
};

export default Chart;
