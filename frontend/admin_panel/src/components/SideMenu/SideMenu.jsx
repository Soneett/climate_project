import React from "react";
import styles from "./SideMenu.module.scss";

export default function SideMenu({ sections, activeSection, onSelect, isOpen, onToggle }) {
  return (
    <div className={styles.wrapper}>
      <button
        className={`${styles.toggleBtn} ${isOpen ? styles.toggleBtnOpen : ""}`}
        onClick={onToggle}
        aria-label={isOpen ? "Закрыть меню" : "Открыть меню"}
        aria-expanded={isOpen}
        type="button"
      >
        {isOpen ? "◀" : "▶"}
      </button>

      <nav
        className={`${styles.menu} ${isOpen ? styles.menuOpen : ""}`}
        aria-label="Навигация по разделам"
      >
        <ul className={styles.list}>
          {sections.map((section) => (
            <li key={section.id}>
              <button
                className={`${styles.menuItem} ${activeSection === section.id ? styles.menuItemActive : ""}`}
                onClick={() => {
                  onSelect(section.id);
                  onToggle();
                }}
                type="button"
              >
                {section.label}
              </button>
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
}
