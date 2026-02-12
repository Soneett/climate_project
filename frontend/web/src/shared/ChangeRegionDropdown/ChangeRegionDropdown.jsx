import React, { useState, useContext, useEffect } from "react";
import Dropdown from "../Dropdown/Dropdown";
import styles from "./ChangeRegionDropdown.module.scss";
import { RegionContext } from "../../context/RegionContext";
import { REGIONS } from "../../constants/regions";

export default function ChangeRegionDropdown() {
  const [open, setOpen] = useState(false);
  const { region, setRegion } = useContext(RegionContext);
  const [selected, setSelected] = useState(region || null);

  useEffect(() => {
    setSelected(region || null);
  }, [region, open]);

  function confirm() {
    if (!selected) return;
    setRegion(selected);
    setOpen(false);
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
          Изменить регион
          <span className={styles.caret} aria-hidden>▾</span>
        </button>
      }
    >
      <div role="menu" aria-label="Сменить регион">
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
    </Dropdown>
  );
}
