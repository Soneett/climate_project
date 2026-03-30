import React from "react";
import PropTypes from "prop-types";
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

ContentBlock.propTypes = {
  id: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  children: PropTypes.node
};

export default React.memo(ContentBlock);
