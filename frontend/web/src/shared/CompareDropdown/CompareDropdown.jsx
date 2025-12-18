import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Dropdown from "../Dropdown/Dropdown";
import styles from "./CompareDropdown.module.scss";
import { REGIONS } from "../../constants/regions";

const CompareDropdown = () => {
  const [open, setOpen] = useState(false);
  const [selected, setSelected] = useState([]);
  const navigate = useNavigate();

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
    <Dropdown
      open={open}
      onOpenChange={setOpen}
      trigger={
        <button
          className={styles.trigger}
          aria-haspopup="true"
          aria-expanded={open}
        >
          Сравнить показатели регионов
          <span className={styles.caret} aria-hidden>▾</span>
        </button>
      }
    >
      <div role="menu" aria-label="Выбор регионов для сравнения">
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
    </Dropdown>
  );
}

export default CompareDropdown
