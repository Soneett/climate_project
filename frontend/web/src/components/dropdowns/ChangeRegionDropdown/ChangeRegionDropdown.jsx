// ChangeRegionDropdown.jsx
import React, { useState, useRef, useEffect, useContext } from "react";
import styles from "./ChangeRegionDropdown.module.scss";
import { RegionContext } from "../../../context/RegionContext";

const REGIONS = [
  "Республика Алтай",
];

export default function ChangeRegionDropdown() {
  const [open, setOpen] = useState(false);
  const { region, setRegion } = useContext(RegionContext);
  const [selected, setSelected] = useState(region || null);
  const rootRef = useRef(null);

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

  useEffect(() => setSelected(region || null), [region, open]);

  function confirm() {
    if (!selected) return;
    setRegion(selected);
    setOpen(false);
  }

  return (
    <div className={styles.root} ref={rootRef}>
      <button
        className={styles.trigger}
        onClick={() => setOpen(o => !o)}
        aria-haspopup="true"
        aria-expanded={open}
      >
        Изменить регион
        <span className={styles.caret} aria-hidden>▾</span>
      </button>

      {open && (
        <div className={styles.panel} role="menu" aria-label="Сменить регион">
          <div className={styles.instructions}>Выберите регион:</div>

          <ul className={styles.list}>
            {REGIONS.map(r => (
              <li key={r} className={styles.item}>
                <label className={styles.label}>
                  <input
                    type="radio"
                    name="region"
                    checked={selected === r}
                    onChange={() => setSelected(r)}
                  />
                  <span className={styles.labelText}>{r}</span>
                </label>
              </li>
            ))}
          </ul>

          <div className={styles.actions}>
            <button className={styles.cancel} onClick={() => setOpen(false)} type="button">Отменить</button>
            <button
              className={styles.confirm}
              onClick={confirm}
              disabled={!selected}
              aria-disabled={!selected}
              type="button"
            >
              Применить
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
