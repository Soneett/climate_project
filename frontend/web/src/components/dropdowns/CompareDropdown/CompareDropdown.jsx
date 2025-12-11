// CompareDropdown.jsx
import React, { useState, useRef, useEffect } from "react";
import styles from "./CompareDropdown.module.scss";
import { useNavigate } from "react-router-dom";

const REGIONS = [
  "Республика Алтай",
  "Свердловская область",
];

const CompareDropdown = () => {
  const [open, setOpen] = useState(false);
  const [selected, setSelected] = useState([]);
  const rootRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    function onClickOutside(e) {
      if (rootRef.current && !rootRef.current.contains(e.target)) setOpen(false);
    }
    function onEsc(e) { if (e.key === "Escape") setOpen(false); }

    document.addEventListener("mousedown", onClickOutside);
    document.addEventListener("keydown", onEsc);
    return () => {
      document.removeEventListener("mousedown", onClickOutside);
      document.removeEventListener("keydown", onEsc);
    };
  }, []);

  function toggle(region) {
    setSelected(prev => (prev.includes(region) ? prev.filter(r => r !== region) : [...prev, region]));
  }

  function confirm() {
    if (selected.length !== 2) return;
    const params = new URLSearchParams({ r1: selected[0], r2: selected[1] });
    setOpen(false);
    navigate(`/compare?${params.toString()}`);
  }

  function clear() {
    setSelected([]);
  }

  return (
    <div className={styles.root} ref={rootRef}>
      <button
        className={styles.trigger}
        onClick={() => setOpen(o => !o)}
        aria-haspopup="true"
        aria-expanded={open}
      >
        Сравнить показатели регионов
        <span className={styles.caret} aria-hidden>▾</span>
      </button>

      {open && (
        <div className={styles.panel} role="menu" aria-label="Выбор регионов для сравнения">
          <div className={styles.instructions}>Выберите 2 региона для сравнения их показателей:</div>

          <ul className={styles.list}>
            {REGIONS.map(r => (
              <li key={r} className={styles.item}>
                <label className={styles.label}>
                  <input
                    type="checkbox"
                    checked={selected.includes(r)}
                    onChange={() => toggle(r)}
                  />
                  <span className={styles.labelText}>{r}</span>
                </label>
              </li>
            ))}
          </ul>

          <div className={styles.actions}>
            <button className={styles.clear} onClick={clear} type="button">Очистить</button>
            <button
              className={styles.confirm}
              onClick={confirm}
              disabled={selected.length !== 2}
              aria-disabled={selected.length !== 2}
              type="button"
            >
              Сравнить
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default CompareDropdown