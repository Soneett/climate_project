import React from "react";
import styles from "./NavigationButton.module.scss";

const NavigationButton = ({ direction = "left", label, onClick, disabled = false }) => {
  const isLeft = direction === "left";
  
  return (
    <button
      className={`${styles.button} ${isLeft ? styles.left : styles.right}`}
      onClick={onClick}
      disabled={disabled}
      aria-label={isLeft ? "Предыдущий раздел" : "Следующий раздел"}
    >
      {isLeft && (
        <svg className={styles.arrow} width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12.5 15L7.5 10L12.5 5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      )}
      <span className={styles.label}>{label}</span>
      {!isLeft && (
        <svg className={styles.arrow} width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M7.5 15L12.5 10L7.5 5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      )}
    </button>
  );
};

export default NavigationButton;
