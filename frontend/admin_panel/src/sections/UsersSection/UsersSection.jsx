import React, { useState } from "react";
import SectionBar from "../../components/SectionBar/SectionBar";
import { MOCK_USERS } from "../../data/mockData";
import styles from "./UsersSection.module.scss";

const ROLE_LABELS = {
  admin: "Администратор",
  editor: "Редактор",
};

function UserRow({ user }) {
  const [showPassword, setShowPassword] = useState(false);

  return (
    <tr className={styles.row}>
      <td className={styles.cell}>{user.id}</td>
      <td className={styles.cell}>{user.name}</td>
      <td className={styles.cell}>{user.email}</td>
      <td className={styles.cell}>{ROLE_LABELS[user.role] ?? user.role}</td>
      <td className={styles.cell}>
        <div className={styles.passwordCell}>
          <span className={styles.passwordValue}>
            {showPassword ? user.password : "••••••••"}
          </span>
          <button
            className={styles.eyeBtn}
            onClick={() => setShowPassword((v) => !v)}
            type="button"
            aria-label={showPassword ? "Скрыть пароль" : "Показать пароль"}
            title={showPassword ? "Скрыть пароль" : "Показать пароль"}
          >
            {showPassword ? "🙈" : "👁"}
          </button>
        </div>
      </td>
    </tr>
  );
}

export default function UsersSection({ users = MOCK_USERS }) {
  return (
    <div className={styles.section}>
      <SectionBar title="Пользователи и роли" />

      <div className={styles.content}>
        <div className={styles.tableWrapper}>
          <table className={styles.table}>
            <thead>
              <tr>
                <th className={styles.th}>id</th>
                <th className={styles.th}>name</th>
                <th className={styles.th}>email</th>
                <th className={styles.th}>role</th>
                <th className={styles.th}>password</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <UserRow key={user.id} user={user} />
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
