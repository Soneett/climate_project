import React, { useEffect, useState } from "react";
import SectionBar from "../../components/SectionBar/SectionBar";
import Modal from "../../shared/Modal/Modal";
import { DB_TABLES, TABLE_PREVIEW_ROWS, INFO_STATS } from "../../data/mockData";
import { getTableChunk, getTableCountFromChunks } from "../../services/api";
import styles from "./InfoSection.module.scss";

function StatsRow({ label, value, hasGapBefore }) {
  return (
    <tr className={`${styles.statsRow} ${hasGapBefore ? styles.statsRowGap : ""}`}>
      <td className={styles.statsCell}>{label}</td>
      <td className={`${styles.statsCell} ${styles.statsCellValue}`}>{value}</td>
    </tr>
  );
}

function TablePreviewCard({ table, previewRows }) {
  const [modalOpen, setModalOpen] = useState(false);

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
  const [tableRowsMap, setTableRowsMap] = useState(TABLE_PREVIEW_ROWS);
  const [liveStats, setLiveStats] = useState(stats);

  useEffect(() => {
    let isMounted = true;

    async function loadInfoData() {
      try {
        const countEntries = await Promise.all(
          DB_TABLES.map(async (table) => {
            const count = await getTableCountFromChunks(table.key);
            return [table.key, Number(count) || 0];
          })
        );

        if (!isMounted) {
          return;
        }

        const countMap = Object.fromEntries(countEntries);
        setLiveStats((prev) => ({
          ...prev,
          totalIndicators: countMap.indicators ?? prev.totalIndicators,
          socialAspects: countMap.indicator_subtypes ?? prev.socialAspects,
          regionalData: countMap.regions ?? prev.regionalData,
          climate: countMap.indicator_values ?? prev.climate,
          governanceAndPolitics: countMap.regional_programs ?? prev.governanceAndPolitics,
        }));

        const rowsEntries = await Promise.all(
          DB_TABLES.map(async (table) => {
            const rows = await getTableChunk(table.key, 3, 0);
            return [table.key, Array.isArray(rows) && rows.length > 0 ? rows : (TABLE_PREVIEW_ROWS[table.key] ?? [])];
          })
        );

        if (!isMounted) {
          return;
        }

        setTableRowsMap(Object.fromEntries(rowsEntries));
      } catch (error) {
        console.error("Failed to load admin info data:", error);
      }
    }

    loadInfoData();
    return () => {
      isMounted = false;
    };
  }, []);

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
              <StatsRow label="Общее число показателей" value={liveStats.totalIndicators} />
              <StatsRow label="Социальные аспекты" value={liveStats.socialAspects} />
              <StatsRow label="Региональные данные" value={liveStats.regionalData} />
              <StatsRow label="Климат" value={liveStats.climate} />
              <StatsRow label="Управление и политика" value={liveStats.governanceAndPolitics} />
              <StatsRow label="Начало периода" value={liveStats.periodStart} hasGapBefore />
              <StatsRow label="Конец периода" value={liveStats.periodEnd} />
              <StatsRow label="Последнее обновление" value={liveStats.lastUpdate} hasGapBefore />
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
                    previewRows={tableRowsMap[table.key] ?? []}
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
