import React from "react";
import PropTypes from "prop-types";
import BlockHeader from "../BlockHeader/BlockHeader";
import styles from "./ContentBlock.module.scss";

/**
 * ContentBlock component
 * Wraps content with a header and provides a scrollable anchor point
 * @param {string} id - Unique identifier for the block (used for scrolling)
 * @param {string} title - Title to display in the block header
 * @param {React.ReactNode} children - Content to display in the block
 */
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
