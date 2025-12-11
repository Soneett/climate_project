// ComparePage.jsx
import React from "react";
import { useLocation } from "react-router-dom";
import styles from "./ComparePage.module.scss";

const ComparePage = () => {
  const { search } = useLocation();
  const params = new URLSearchParams(search);
  const r1 = params.get("r1") || "—";
  const r2 = params.get("r2") || "—";

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <div className={styles.inner}></div>
      </header>

      <main className={styles.main}>
        <h2 className={styles.title}>Сравнение: {r1} vs {r2}</h2>
      </main>
    </div>
  );
}

export default ComparePage
