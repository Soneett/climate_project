import React from "react";
import BlockHeader from "../BlockHeader/BlockHeader";
import Chart from "../Chart/Chart";
import LineChart from "../Charts/LineChart/LineChart.jsx";
import styles from "./ContentBlock.module.scss";

const ContentBlock = ({ id, title, chartType = "line" }) => {
  return (
    <section className={styles.block} id={id}>
      <BlockHeader title={title} />
      <LineChart type={chartType} />
      {/*<Chart type={chartType} />*/}
    </section>
  );
};

export default ContentBlock;
