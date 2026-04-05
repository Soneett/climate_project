import React, { useState } from "react";
import SectionBar from "../../components/SectionBar/SectionBar";
import { DB_TABLES } from "../../data/mockData";
import { fetchUploadIndicators, uploadIndicatorFile } from "../../services/api";
import styles from "./LoadDataSection.module.scss";

const REGIONS_LIST = [
  "Свердловская область", "Республика Алтай",
];

const DATA_SOURCES_LIST = ["МЧС", "Росстат",];

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
  const [region, setRegion] = useState("");
  const [indicatorKey, setIndicatorKey] = useState("");
  const [source, setSource] = useState("");
  const [file, setFile] = useState(null);
  const [indicators, setIndicators] = useState([]);
  const [isLoadingIndicators, setIsLoadingIndicators] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [status, setStatus] = useState("");
  const [statusType, setStatusType] = useState("default");

  const allSelected = region && indicatorKey && source;

  React.useEffect(() => {
    let isMounted = true;

    const loadIndicators = async () => {
      setIsLoadingIndicators(true);
      setStatus("");
      try {
        const payload = await fetchUploadIndicators();
        if (!isMounted) {
          return;
        }
        setIndicators(Array.isArray(payload) ? payload : []);
      } catch (error) {
        if (!isMounted) {
          return;
        }
        setStatus(error.message || "Не удалось загрузить показатели.");
        setStatusType("error");
      } finally {
        if (isMounted) {
          setIsLoadingIndicators(false);
        }
      }
    };

    loadIndicators();

    return () => {
      isMounted = false;
    };
  }, []);

  function handleFileChange(e) {
    setFile(e.target.files[0] || null);
  }

  async function handleUpload() {
    if (!file || !indicatorKey) {
      return;
    }

    setIsUploading(true);
    setStatus("");
    try {
      const result = await uploadIndicatorFile({ indicatorKey, file });
      setStatusType("success");
      setStatus(
        `Файл загружен: добавлено ${result.uploaded ?? 0}, пропущено ${result.skipped ?? 0}.`
      );
    } catch (error) {
      setStatusType("error");
      setStatus(error.message || "Ошибка при загрузке файла.");
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
          aria-label="Выберите показатель"
          disabled={isLoadingIndicators}
        >
          <option value="">
            {isLoadingIndicators ? "Загрузка показателей..." : "Выберите показатель"}
          </option>
          {indicators.map((item) => (
            <option key={item.key} value={item.key}>{item.name}</option>
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
            disabled={!file || isUploading}
            onClick={handleUpload}
          >
            {isUploading ? "Загрузка..." : "Загрузить данные"}
          </button>
        </div>
      )}

      {status && (
        <p
          style={{
            marginTop: 12,
            color: statusType === "error" ? "#b42318" : "#166534",
            fontWeight: 600
          }}
        >
          {status}
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
