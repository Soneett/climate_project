import React, { useEffect, useMemo, useState } from "react";
import SectionBar from "../../components/SectionBar/SectionBar";
import { DB_TABLES } from "../../data/mockData";
import { getUploadIndicators, uploadIndicatorData } from "../../services/dataUploadApi";
import styles from "./LoadDataSection.module.scss";

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

function ChartsUploadPart() {
  const [indicatorOptions, setIndicatorOptions] = useState([]);
  const [chart, setChart] = useState("");
  const [file, setFile] = useState(null);
  const [loadingIndicators, setLoadingIndicators] = useState(true);
  const [isUploading, setIsUploading] = useState(false);
  const [status, setStatus] = useState(null);

  useEffect(() => {
    let isCancelled = false;

    async function loadIndicators() {
      setLoadingIndicators(true);
      try {
        const indicators = await getUploadIndicators();
        if (!isCancelled) {
          setIndicatorOptions(indicators);
          if (indicators.length > 0) {
            setChart(indicators[0].key);
          }
        }
      } catch (error) {
        if (!isCancelled) {
          setStatus({ type: "error", message: error.message });
        }
      } finally {
        if (!isCancelled) {
          setLoadingIndicators(false);
        }
      }
    }

    loadIndicators();

    return () => {
      isCancelled = true;
    };
  }, []);

  const selectedIndicator = useMemo(
    () => indicatorOptions.find((indicator) => indicator.key === chart),
    [indicatorOptions, chart]
  );

  const canUpload = chart && file && !isUploading;

  function handleFileChange(e) {
    setFile(e.target.files[0] || null);
    setStatus(null);
  }

  async function handleUpload() {
    if (!canUpload) {
      return;
    }

    setIsUploading(true);
    setStatus(null);

    try {
      const result = await uploadIndicatorData({ file, indicatorKey: chart });
      setStatus({
        type: "success",
        message: `Файл обработан. Добавлено: ${result.uploaded}, пропущено: ${result.skipped}.`,
      });
      setFile(null);
    } catch (error) {
      setStatus({ type: "error", message: error.message });
    } finally {
      setIsUploading(false);
    }
  }

  return (
    <div className={styles.partContent}>
      <div className={styles.selectorsRow}>
        <select
          className={styles.selector}
          value={chart}
          onChange={(e) => {
            setChart(e.target.value);
            setStatus(null);
          }}
          aria-label="Выберите показатель"
          disabled={loadingIndicators || indicatorOptions.length === 0}
        >
          <option value="">
            {loadingIndicators ? "Загружаем список показателей..." : "Выберите показатель"}
          </option>
          {indicatorOptions.map((item) => (
            <option key={item.key} value={item.key}>{item.label}</option>
          ))}
        </select>
      </div>

      {chart && (
        <div className={styles.uploadRow}>
          <label className={styles.fileLabel}>
            <input
              type="file"
              accept=".xlsx,.xls,.xlsm,.xlsb"
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
          <button
            className={styles.loadBtn}
            type="button"
            aria-label="Загрузить данные"
            onClick={handleUpload}
            disabled={!canUpload}
          >
            {isUploading ? "Загружаем..." : "Загрузить данные"}
          </button>
        </div>
      )}

      {selectedIndicator && (
        <p className={styles.fileName}>Показатель: {selectedIndicator.label}</p>
      )}

      {status && (
        <p className={status.type === "success" ? styles.fileName : styles.errorText}>
          {status.message}
        </p>
      )}
    </div>
  );
}

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
