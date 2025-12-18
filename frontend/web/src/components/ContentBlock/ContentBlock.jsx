import React from "react";
import BlockHeader from "../BlockHeader/BlockHeader";
import Chart from "../Chart/Chart";
import styles from "./ContentBlock.module.scss";

const ContentBlock = ({ id, title, chartType = "bar" }) => {
  return (
    <section className={styles.block} id={id}>
      <BlockHeader title={title} />
      <Chart type={chartType} />
    </section>
  );
};

export default ContentBlock;
