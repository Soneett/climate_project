import React from "react";
import BlockHeader from "../BlockHeader/BlockHeader";
import styles from "./ContentBlock.module.scss";

const ContentBlock = ({ id, title, children }) => {
  return (
    <section className={styles.block} id={id}>
      <BlockHeader title={title} />
      {children}
    </section>
  );
};

export default ContentBlock;
