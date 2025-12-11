// HomePage.jsx
import React, { useContext } from "react";
import styles from "./HomePage.module.scss";
import { RegionContext } from "../../context/RegionContext";

export default function HomePage() {
  const { region } = useContext(RegionContext);

  return (
    <main className={styles.hero} role="main" aria-label="Главная">
      <div className={styles.overlay}>
        <h1 className={styles.title}>
          Социально-климатический профиль
          <br />
          <span className={styles.region}>{region}</span>
        </h1>
      </div>
    </main>
  );
}
