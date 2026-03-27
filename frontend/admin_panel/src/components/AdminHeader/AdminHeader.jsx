import React from "react";
import { useAuth } from "../../context/AuthContext";
import styles from "./AdminHeader.module.scss";

const ROLE_LABELS = {
  admin: "Администратор",
  editor: "Редактор",
};

export default function AdminHeader() {
  const { currentUser, logout } = useAuth();

  return (
    <header className={styles.header}>
      <div className={styles.inner}>
        <div className={styles.userInfo}>
          <div className={styles.avatar} aria-label="Аватар пользователя">
            {currentUser?.name ? currentUser.name[0].toUpperCase() : "?"}
          </div>
          <span className={styles.role}>
            {ROLE_LABELS[currentUser?.role] ?? currentUser?.role}
          </span>
        </div>

        <button className={styles.logoutBtn} onClick={logout} type="button">
          Выйти
        </button>
      </div>
    </header>
  );
}
