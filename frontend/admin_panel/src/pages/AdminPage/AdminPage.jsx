import React, { useState } from "react";
import { useAuth } from "../../context/AuthContext";
import AdminHeader from "../../components/AdminHeader/AdminHeader";
import SideMenu from "../../components/SideMenu/SideMenu";
import InfoSection from "../../sections/InfoSection/InfoSection";
import UsersSection from "../../sections/UsersSection/UsersSection";
import LoadDataSection from "../../sections/LoadDataSection/LoadDataSection";
import CleanDataSection from "../../sections/CleanDataSection/CleanDataSection";
import HistorySection from "../../sections/HistorySection/HistorySection";
import styles from "./AdminPage.module.scss";

// ============================================================================
// Sections config — filtered by role
// ============================================================================
const ALL_SECTIONS = [
  { id: "info", label: "Информация", roles: ["admin", "editor"] },
  { id: "users", label: "Пользователи и роли", roles: ["admin"] },
  { id: "load", label: "Загрузка и обновление данных", roles: ["admin", "editor"] },
  { id: "clean", label: "Очистка и архивация данных", roles: ["admin", "editor"] },
  { id: "history", label: "История изменений", roles: ["admin", "editor"] },
];

export default function AdminPage() {
  const { currentUser } = useAuth();
  const role = currentUser?.role ?? "editor";

  const availableSections = ALL_SECTIONS.filter((s) => s.roles.includes(role));
  const [activeSection, setActiveSection] = useState(availableSections[0]?.id ?? "info");
  const [menuOpen, setMenuOpen] = useState(false);

  function handleSectionSelect(id) {
    setActiveSection(id);
  }

  function handleMenuToggle() {
    setMenuOpen((v) => !v);
  }

  function renderSection() {
    switch (activeSection) {
      case "info":
        return <InfoSection />;
      case "users":
        return <UsersSection />;
      case "load":
        return <LoadDataSection role={role} />;
      case "clean":
        return <CleanDataSection />;
      case "history":
        return <HistorySection />;
      default:
        return null;
    }
  }

  return (
    <div className={styles.page}>
      <AdminHeader />

      <div className={styles.body}>
        <SideMenu
          sections={availableSections}
          activeSection={activeSection}
          onSelect={handleSectionSelect}
          isOpen={menuOpen}
          onToggle={handleMenuToggle}
        />

        <main className={`${styles.main} ${menuOpen ? styles.mainShifted : ""}`}>
          {renderSection()}
        </main>
      </div>
    </div>
  );
}
