import React, { useEffect, useMemo, useState } from "react";
import SectionBar from "../../components/SectionBar/SectionBar";
import { DB_TABLES } from "../../data/mockData";
import { deleteIndicatorValueById, getUploadIndicators, uploadDataFile } from "../../services/api";
import styles from "./LoadDataSection.module.scss";

const REGIONS_LIST = [
  "Свердловская область", "Республика Алтай",
];

const DATA_SOURCES_LIST = ["МЧС", "Росстат",];

function TableManageCard({ table, indicatorOptions }) {
  const [indicatorIdToDelete, setIndicatorIdToDelete] = useState("");
  const [indicatorKey, setIndicatorKey] = useState("");
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");

  async function handleDeleteIndicator() {
    if (table.key !== "indicator_values" || !indicatorIdToDelete) {
      setStatus("Удаление отдельных показателей доступно для indicator_values.");
      return;
    }

    try {
      await deleteIndicatorValueById(indicatorIdToDelete);
      setStatus(`Показатель id=${indicatorIdToDelete} удалён из БД.`);
      setIndicatorIdToDelete("");
    } catch (error) {
      console.error("Ошибка удаления показателя:", error);
      setStatus("Не удалось удалить показатель. Проверьте ID.");
    }
  }

  async function handleUploadIndicator() {
    if (!file || !indicatorKey) {
      setStatus("Выберите парсер и файл.");
      return;
    }

    try {
      const result = await uploadDataFile({ file, indicatorKey });
      setStatus(`Данные загружены: ${result.uploaded}, пропущено: ${result.skipped}.`);
      setFile(null);
      setIndicatorKey("");
    } catch (error) {
      console.error("Ошибка загрузки показателя:", error);
      setStatus("Не удалось загрузить файл показателя.");
    }
  }

  return (
    <div className={styles.manageCard}>
      <h3 className={styles.manageCardTitle}>{table.labelRu}</h3>
      <div className={styles.manageActions}>
        <button className={styles.actionBtn} type="button">➕ Новая запись</button>
        <button className={styles.actionBtn} type="button">✏️ Изменить запись</button>

        <select
          className={styles.selector}
          value={indicatorKey}
          onChange={(e) => setIndicatorKey(e.target.value)}
          aria-label="Выберите парсер"
        >
          <option value="">Выберите парсер</option>
          {indicatorOptions.map((option) => (
            <option key={option.key} value={option.key}>{option.label}</option>
          ))}
        </select>

        <label className={styles.fileLabel}>
          <input
            type="file"
            accept=".pdf,.xlsx,.xls"
            className={styles.fileInput}
            onChange={(e) => setFile(e.target.files?.[0] || null)}
          />
          <span className={styles.fileLabelText}>⬆️ {file ? file.name : "Файл показателя"}</span>
        </label>

        <button className={styles.actionBtn} type="button" onClick={handleUploadIndicator}>⬆️ Загрузить показатель</button>

        <input
          type="number"
          placeholder="ID показателя"
          className={styles.selector}
          value={indicatorIdToDelete}
          onChange={(e) => setIndicatorIdToDelete(e.target.value)}
        />
        <button className={`${styles.actionBtn} ${styles.actionBtnDanger}`} type="button" onClick={handleDeleteIndicator}>🗑 Удалить показатель</button>
      </div>
      {status && <p>{status}</p>}
    </div>
  );
}

function TablesManagePart({ indicatorOptions }) {
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
            {openTableKey === table.key && <TableManageCard table={table} indicatorOptions={indicatorOptions} />}
          </div>
        ))}
      </div>
    </div>
  );
}

function ChartsUploadPart({ indicatorOptions }) {
  const [region, setRegion] = useState("");
  const [indicatorKey, setIndicatorKey] = useState("");
  const [source, setSource] = useState("");
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");
  const [isUploading, setIsUploading] = useState(false);

  const allSelected = region && indicatorKey && source;

  const selectedIndicatorLabel = useMemo(
    () => indicatorOptions.find((item) => item.key === indicatorKey)?.label || "",
    [indicatorKey, indicatorOptions]
  );

  function handleFileChange(e) {
    setFile(e.target.files[0] || null);
  }

  async function handleUpload() {
    if (!file || !indicatorKey) {
      return;
    }

    setIsUploading(true);
    setUploadStatus("");
    try {
      const result = await uploadDataFile({ file, indicatorKey });
      setUploadStatus(
        `Файл обработан (${selectedIndicatorLabel || indicatorKey}): загружено ${result.uploaded}, пропущено ${result.skipped}.`
      );
    } catch (error) {
      console.error("Ошибка загрузки файла:", error);
      setUploadStatus("Не удалось загрузить файл. Проверьте формат файла и выбранный парсер.");
    } finally {
      setIsUploading(false);
    }
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
          value={indicatorKey}
          onChange={(e) => setIndicatorKey(e.target.value)}
          aria-label="Выберите парсер"
        >
          <option value="">Выберите показатель/парсер</option>
          {indicatorOptions.map((option) => (
            <option key={option.key} value={option.key}>{option.label}</option>
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
          <button
            className={styles.loadBtn}
            type="button"
            aria-label="Загрузить данные"
            onClick={handleUpload}
            disabled={!file || isUploading}
          >
            Загрузить данные
          </button>
        </div>
      )}
      {uploadStatus && <p>{uploadStatus}</p>}
    </div>
  );
}

export default function LoadDataSection({ role }) {
  const [indicatorOptions, setIndicatorOptions] = useState([]);

  useEffect(() => {
    let isMounted = true;
    getUploadIndicators()
      .then((response) => {
        if (isMounted && Array.isArray(response)) {
          setIndicatorOptions(response);
        }
      })
      .catch((error) => {
        console.error("Не удалось загрузить список парсеров:", error);
      });

    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <div className={styles.section}>
      <SectionBar title="Загрузка и обновление данных таблиц" />

      <div className={styles.content}>
        {role === "admin" && (
          <div className={styles.part}>
            <TablesManagePart indicatorOptions={indicatorOptions} />
          </div>
        )}

        <div className={styles.part}>
          <SectionBar title="Загрузка и обновление данных графиков" />
          <ChartsUploadPart indicatorOptions={indicatorOptions} />
        </div>
      </div>
    </div>
  );
}
