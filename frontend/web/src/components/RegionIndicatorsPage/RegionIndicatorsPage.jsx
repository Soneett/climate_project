import React, { useState, useEffect } from "react";
import NavBar from "../NavBar/NavBar";
import SecondarySubBar from "../SecondarySubBar/SecondarySubBar";
import styles from "./RegionIndicatorsPage.module.scss";

const TOP_MENUS = [
  { id: "regional", label: "Региональные\nданные", submenu: [] },
  { id: "social", label: "Социальные\nаспекты", submenu: [
      { id: "s1", label: "Демография" },
      { id: "s2", label: "Уровень жизни" },
      { id: "s3", label: "Здравоохранение" },
      { id: "s4", label: "Образование" },
      { id: "s5", label: "Экономика" },
      { id: "s6", label: "Инфраструктура" },
    ] },
  { id: "climate", label: "Климат", submenu: [
      { id: "c1", label: "Температура" },
      { id: "c2", label: "Осадки" },
      { id: "c3", label: "Ветер" },
      { id: "c4", label: "Природные катаклизмы" },
      { id: "c5", label: "Экология" },
    ] },
  { id: "governance", label: "Управление и\nполитика", submenu: [
      { id: "g1", label: "Бюджет" },
      { id: "g2", label: "Региональные программы развития" },
      { id: "g3", label: "Федеральные программы" },
      { id: "g4", label: "Программы адаптации к климатическим изменениям" },
    ] },
  { id: "relations", label: "Взаимосвязи", submenu: [] },
];

export default function RegionIndicatorsPage() {
  const [activeTopMenuId, setActiveTopMenuId] = useState(null);
  const [activeSubItemId, setActiveSubItemId] = useState(null);

  const activeMenu = TOP_MENUS.find(m => m.id === activeTopMenuId);

  // Автоматический выбор "Социальные аспекты" и первого подпункта при монтировании
  useEffect(() => {
    const defaultTop = TOP_MENUS.find(m => m.id === "social") || TOP_MENUS[0];
    setActiveTopMenuId(defaultTop.id);
    if (defaultTop.submenu && defaultTop.submenu.length > 0) {
      setActiveSubItemId(defaultTop.submenu[0].id);
    }
  }, []);

  // Выбор верхнего меню
  const handleTopMenuChange = (newId) => {
    if (!newId) return;
    setActiveTopMenuId(newId);
    const menu = TOP_MENUS.find(m => m.id === newId);
    if (menu.submenu && menu.submenu.length > 0) {
      setActiveSubItemId(menu.submenu[0].id);
    } else {
      setActiveSubItemId(null);
    }
  };

  return (
    <div className={styles.page}>
      <NavBar
        mode="indicators"
        topMenus={TOP_MENUS}
        activeTopMenuId={activeTopMenuId}
        onTopMenuChange={handleTopMenuChange}
      />

      {activeMenu && activeMenu.submenu && activeMenu.submenu.length > 0 && (
        <SecondarySubBar
          items={activeMenu.submenu}
          activeId={activeSubItemId}
          onSelect={setActiveSubItemId}
        />
      )}

      <main className={styles.main}>
        {activeMenu && activeSubItemId && (
          <section className={styles.content}>
            <h2>
              {activeMenu.label.replace("\n", " ")} — {activeMenu.submenu.find(s => s.id === activeSubItemId)?.label}
            </h2>
          </section>
        )}
      </main>
    </div>
  );
}
