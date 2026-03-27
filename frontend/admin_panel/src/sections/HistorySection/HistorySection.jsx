import React, { useState } from "react";
import SectionBar from "../../components/SectionBar/SectionBar";
import { MOCK_HISTORY } from "../../data/mockData";
import styles from "./HistorySection.module.scss";

function HistoryCard({ entry }) {
  return (
    <div className={styles.card}>
      <div className={styles.cardTarget}>{entry.targetRu || entry.target}</div>
      <div className={styles.cardMeta}>
        <span className={styles.cardEmail}>{entry.userEmail}</span>
        <span className={styles.cardDate}>{entry.date}</span>
      </div>
    </div>
  );
}

export default function HistorySection({ history = MOCK_HISTORY }) {
  const [sortOrder, setSortOrder] = useState("desc");

  const sorted = [...history].sort((a, b) => {
    const parseDate = (d) => {
      const [day, month, year] = d.split(".");
      return new Date(`${year}-${month}-${day}`);
    };
    const diff = parseDate(a.date) - parseDate(b.date);
    return sortOrder === "desc" ? -diff : diff;
  });

  return (
    <div className={styles.section}>
      <SectionBar title="История изменений" />

      <div className={styles.content}>
        <div className={styles.filterRow}>
          <button
            className={`${styles.filterBtn} ${sortOrder === "desc" ? styles.filterBtnActive : ""}`}
            onClick={() => setSortOrder("desc")}
            type="button"
          >
            Фильтр: по дате ↓
          </button>
          <button
            className={`${styles.filterBtn} ${sortOrder === "asc" ? styles.filterBtnActive : ""}`}
            onClick={() => setSortOrder("asc")}
            type="button"
          >
            Фильтр: по дате ↑
          </button>
        </div>

        <div className={styles.list}>
          {sorted.map((entry) => (
            <HistoryCard key={entry.id} entry={entry} />
          ))}
        </div>
      </div>
    </div>
  );
}
