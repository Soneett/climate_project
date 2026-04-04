import React, { useState } from "react";
import SectionBar from "../../components/SectionBar/SectionBar";
import Modal from "../../shared/Modal/Modal";
import { DB_TABLES, TABLE_PREVIEW_ROWS, INFO_STATS } from "../../data/mockData";
import styles from "./InfoSection.module.scss";

function StatsRow({ label, value, hasGapBefore }) {
  return (
    <tr className={`${styles.statsRow} ${hasGapBefore ? styles.statsRowGap : ""}`}>
      <td className={styles.statsCell}>{label}</td>
      <td className={`${styles.statsCell} ${styles.statsCellValue}`}>{value}</td>
    </tr>
  );
}

function TablePreviewCard({ table, onClose }) {
  const [modalOpen, setModalOpen] = useState(false);
  const previewRows = TABLE_PREVIEW_ROWS[table.key] ?? [];

  return (
    <div className={styles.previewCard}>
      <h3 className={styles.previewTitle}>{table.labelRu}</h3>

      <div className={styles.previewTableWrapper}>
        <table className={styles.previewTable}>
          <thead>
            <tr>
              {table.columns.map((col) => (
                <th key={col} className={styles.previewTh}>{col}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {previewRows.length > 0 ? (
              previewRows.map((row, idx) => (
                <tr key={idx}>
                  {table.columns.map((col) => (
                    <td key={col} className={styles.previewTd}>
                      {String(row[col] ?? "")}
                    </td>
                  ))}
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={table.columns.length} className={styles.previewTd}>
                  Данные загружаются с сервера...
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <button
        className={styles.viewAllBtn}
        onClick={() => setModalOpen(true)}
        type="button"
      >
        Посмотреть все содержимое
      </button>

      <Modal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        title={table.labelRu}
      >
        <div className={styles.modalTableWrapper}>
          <table className={styles.previewTable}>
            <thead>
              <tr>
                {table.columns.map((col) => (
                  <th key={col} className={styles.previewTh}>{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {previewRows.length > 0 ? (
                previewRows.map((row, idx) => (
                  <tr key={idx}>
                    {table.columns.map((col) => (
                      <td key={col} className={styles.previewTd}>
                        {String(row[col] ?? "")}
                      </td>
                    ))}
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={table.columns.length} className={styles.previewTd}>
                    Данные будут загружены с сервера
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </Modal>
    </div>
  );
}

export default function InfoSection({ stats = INFO_STATS }) {
  const [openTableKey, setOpenTableKey] = useState(null);

  function handleTableToggle(key) {
    setOpenTableKey((prev) => (prev === key ? null : key));
  }

  return (
    <div className={styles.section}>
      <SectionBar title="Информация" />

      <div className={styles.content}>

        <div className={styles.statsTableWrapper}>
          <table className={styles.statsTable}>
            <tbody>
              <StatsRow label="Общее число показателей" value={stats.totalIndicators} />
              <StatsRow label="Социальные аспекты" value={stats.socialAspects} />
              <StatsRow label="Региональные данные" value={stats.regionalData} />
              <StatsRow label="Климат" value={stats.climate} />
              <StatsRow label="Управление и политика" value={stats.governanceAndPolitics} />
              <StatsRow label="Начало периода" value={stats.periodStart} hasGapBefore />
              <StatsRow label="Конец периода" value={stats.periodEnd} />
              <StatsRow label="Последнее обновление" value={stats.lastUpdate} hasGapBefore />
            </tbody>
          </table>
        </div>

        <div className={styles.tablesBlock}>
          <div className={styles.tablesBar}>
            <span className={styles.tablesBarText}>Таблицы</span>
          </div>

          <div className={styles.tablesContainer}>
            {DB_TABLES.map((table) => (
              <div key={table.key}>
                <button
                  className={`${styles.tableItem} ${openTableKey === table.key ? styles.tableItemActive : ""}`}
                  onClick={() => handleTableToggle(table.key)}
                  type="button"
                >
                  {table.labelEn}
                </button>

                {openTableKey === table.key && (
                  <TablePreviewCard
                    table={table}
                    onClose={() => setOpenTableKey(null)}
                  />
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
