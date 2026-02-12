// ComparePage.jsx
import React from "react";
import { useLocation } from "react-router-dom";
import Layout from "../../shared/Layout/Layout";
import styles from "./ComparePage.module.scss";

const ComparePage = () => {
  const { search } = useLocation();
  const params = new URLSearchParams(search);
  const r1 = params.get("r1") || "—";
  const r2 = params.get("r2") || "—";

  return (
    <Layout>
      <div className={styles.page}>
        <main className={styles.main}>
          <h2 className={styles.title}>Сравнение: {r1} vs {r2}</h2>
        </main>
      </div>
    </Layout>
  );
}

export default ComparePage
