import React from "react";
import styles from "./SecondarySubBar.module.scss";

const SecondarySubBar = ({ items = [], activeId = null, onSelect = () => {} }) => {
  if (!items || items.length === 0) return null;

  return (
    <nav className={styles.bar} aria-label="Вторичная навигация">
      <div className={styles.inner}>
        {items.map(it => (
          <button
            key={it.id}
            type="button"
            className={`${styles.cell} ${activeId === it.id ? styles.active : ""}`}
            onClick={() => onSelect(it.id)}
          >
            <span className={styles.text}>{it.label}</span>
          </button>
        ))}
      </div>
    </nav>
  );
};

export default SecondarySubBar;
