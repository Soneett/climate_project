import React, { useState } from "react";
import SectionBar from "../../components/SectionBar/SectionBar";
import { DB_TABLES } from "../../data/mockData";
import styles from "./CleanDataSection.module.scss";

function TableCleanCard({ table }) {
  return (
    <div className={styles.cleanCard}>
      <div className={styles.cleanActions}>
        <button className={`${styles.cleanBtn} ${styles.cleanBtnWarn}`} type="button">
          Очистить таблицу
        </button>
        <button className={`${styles.cleanBtn} ${styles.cleanBtnNeutral}`} type="button">
          Архивировать таблицу
        </button>
      </div>
    </div>
  );
}

export default function CleanDataSection() {
  const [openTableKey, setOpenTableKey] = useState(null);

  function handleToggle(key) {
    setOpenTableKey((prev) => (prev === key ? null : key));
  }

  return (
    <div className={styles.section}>
      <SectionBar title="Очистка и архивация данных" />

      <div className={styles.content}>
        <div className={styles.tablesList}>
          {DB_TABLES.map((table) => (
            <div key={table.key}>
              <button
                className={`${styles.tableItem} ${openTableKey === table.key ? styles.tableItemActive : ""}`}
                onClick={() => handleToggle(table.key)}
                type="button"
              >
                {table.labelEn}
              </button>
              {openTableKey === table.key && <TableCleanCard table={table} />}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
