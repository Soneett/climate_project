import React from "react";
import styles from "./SectionBar.module.scss";

export default function SectionBar({ title }) {
  return (
    <div className={styles.bar}>
      <span className={styles.title}>{title}</span>
    </div>
  );
}
