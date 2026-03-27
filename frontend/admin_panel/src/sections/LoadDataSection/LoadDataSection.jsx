import React, { useState } from "react";
import SectionBar from "../../components/SectionBar/SectionBar";
import { DB_TABLES } from "../../data/mockData";
import styles from "./LoadDataSection.module.scss";

// ============================================================================
// Mock selectors data — replace with real data from API / site config
// ============================================================================
const REGIONS_LIST = [
  "Свердловская область", "Республика Алтай",
];

const CHARTS_LIST = [
  "Численность населения", "ВРП на душу населения",
];

const DATA_SOURCES_LIST = ["МЧС", "Росстат",];

// ============================================================================
// Admin-only: table management card
// ============================================================================
function TableManageCard({ table }) {
  return (
    <div className={styles.manageCard}>
      <h3 className={styles.manageCardTitle}>{table.labelRu}</h3>
      <div className={styles.manageActions}>
        <button className={styles.actionBtn} type="button">➕ Новая запись</button>
        <button className={styles.actionBtn} type="button">✏️ Изменить запись</button>
        <button className={styles.actionBtn} type="button">⬆️ Загрузить данные</button>
        <button className={`${styles.actionBtn} ${styles.actionBtnDanger}`} type="button">🗑 Удалить таблицу</button>
      </div>
    </div>
  );
}

// ============================================================================
// Admin-only part: tables management
// ============================================================================
function TablesManagePart() {
  const [openTableKey, setOpenTableKey] = useState(null);

  function handleToggle(key) {
    setOpenTableKey((prev) => (prev === key ? null : key));
  }

  return (
    <div className={styles.partContent}>
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
            {openTableKey === table.key && <TableManageCard table={table} />}
          </div>
        ))}
      </div>
    </div>
  );
}

// ============================================================================
// Charts upload part (admin + editor)
// ============================================================================
function ChartsUploadPart() {
  const [region, setRegion] = useState("");
  const [chart, setChart] = useState("");
  const [source, setSource] = useState("");
  const [file, setFile] = useState(null);

  const allSelected = region && chart && source;

  function handleFileChange(e) {
    setFile(e.target.files[0] || null);
  }

  return (
    <div className={styles.partContent}>
      <div className={styles.selectorsRow}>
        <select
          className={styles.selector}
          value={region}
          onChange={(e) => setRegion(e.target.value)}
          aria-label="Выберите регион"
        >
          <option value="">Выберите регион</option>
          {REGIONS_LIST.map((r) => (
            <option key={r} value={r}>{r}</option>
          ))}
        </select>

        <select
          className={styles.selector}
          value={chart}
          onChange={(e) => setChart(e.target.value)}
          aria-label="Выберите название графика"
        >
          <option value="">Выберите название графика</option>
          {CHARTS_LIST.map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>

        <select
          className={styles.selector}
          value={source}
          onChange={(e) => setSource(e.target.value)}
          aria-label="Выберите источник данных"
        >
          <option value="">Выберите источник данных</option>
          {DATA_SOURCES_LIST.map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
      </div>

      {allSelected && (
        <div className={styles.uploadRow}>
          <label className={styles.fileLabel}>
            <input
              type="file"
              accept=".pdf,.xlsx,.xls"
              className={styles.fileInput}
              onChange={handleFileChange}
            />
            <span className={styles.fileLabelText}>
              ⬆️ {file ? file.name : "Выбрать файл"}
            </span>
          </label>
          {file && (
            <span className={styles.fileName}>{file.name}</span>
          )}
          <button className={styles.loadBtn} type="button" aria-label="Загрузить данные">
            Загрузить данные
          </button>
        </div>
      )}
    </div>
  );
}

// ============================================================================
// Main LoadDataSection
// ============================================================================
export default function LoadDataSection({ role }) {
  return (
    <div className={styles.section}>
      <SectionBar title="Загрузка и обновление данных таблиц" />

      <div className={styles.content}>
        {role === "admin" && (
          <div className={styles.part}>
            <TablesManagePart />
          </div>
        )}

        <div className={styles.part}>
          <SectionBar title="Загрузка и обновление данных графиков" />
          <ChartsUploadPart />
        </div>
      </div>
    </div>
  );
}
