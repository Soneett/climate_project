import React, { useState } from "react";
import styles from "./PageNavigationMenu.module.scss";

const PageNavigationMenu = ({ blocks = [] }) => {
  const [isOpen, setIsOpen] = useState(false);

  const scrollToBlock = (blockId) => {
    const element = document.getElementById(blockId);
    if (element) {
      element.scrollIntoView({ behavior: "smooth", block: "start" });
      setIsOpen(false);
    }
  };

  if (blocks.length === 0) return null;

  return (
    <div className={styles.menu}>
      <button
        className={styles.toggle}
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Навигация по странице"
        aria-expanded={isOpen}
      >
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M3 12H21M3 6H21M3 18H21" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </button>

      {isOpen && (
        <nav className={styles.dropdown} aria-label="Навигация по блокам">
          <ul className={styles.list}>
            {blocks.map((block) => (
              <li key={block.id} className={styles.item}>
                <button
                  className={styles.link}
                  onClick={() => scrollToBlock(block.id)}
                >
                  {block.title}
                </button>
              </li>
            ))}
          </ul>
        </nav>
      )}
    </div>
  );
};

export default PageNavigationMenu;
