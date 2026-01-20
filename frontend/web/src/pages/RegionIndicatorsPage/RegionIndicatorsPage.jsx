import React, { useState, useEffect } from "react";
import NavBar from "../../components/NavBar/NavBar";
import SecondarySubBar from "../../components/SecondarySubBar/SecondarySubBar";
import RelationsSubBar from "../../components/RelationsSubBar/RelationsSubBar";
import ContentBlock from "../../components/ContentBlock/ContentBlock";
import LineChart from "../../components/Charts/LineChart/LineChart";
import PieChart from "../../components/Charts/PieChart/PieChart";
import NavigationButton from "../../components/NavigationButton/NavigationButton";
import PageNavigationMenu from "../../components/PageNavigationMenu/PageNavigationMenu";
import { CONTENT_BLOCKS } from "../../constants/contentBlocks";
import { RELATIONS_CONTENT } from "../../constants/relationsConfig";
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
  const [selectedSubject, setSelectedSubject] = useState(null);
  const [selectedObject, setSelectedObject] = useState(null);

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
    // Reset relations selection when changing menu
    setSelectedSubject(null);
    setSelectedObject(null);
    // Scroll to top instantly
    window.scrollTo({ top: 0, behavior: "instant" });
  };

  // Handle relations selection
  const handleRelationsSelection = (subjectId, objectId) => {
    setSelectedSubject(subjectId);
    setSelectedObject(objectId);
    // Scroll to top instantly
    window.scrollTo({ top: 0, behavior: "instant" });
  };

  // Get current section ID (submenu item or top menu item)
  const getCurrentSectionId = () => {
    if (activeSubItemId) return activeSubItemId;
    if (activeTopMenuId) return activeTopMenuId;
    return null;
  };

  // Get navigation info
  const getNavigationInfo = () => {
    const currentSectionId = getCurrentSectionId();
    if (!currentSectionId) return { prev: null, next: null };

    // Find all sections (flatten structure)
    const allSections = [];
    TOP_MENUS.forEach(menu => {
      if (menu.submenu && menu.submenu.length > 0) {
        menu.submenu.forEach(sub => {
          allSections.push({ id: sub.id, label: sub.label, parentId: menu.id });
        });
      } else {
        allSections.push({ id: menu.id, label: menu.label.replace("\n", " "), parentId: null });
      }
    });

    const currentIndex = allSections.findIndex(s => s.id === currentSectionId);
    const prev = currentIndex > 0 ? allSections[currentIndex - 1] : null;
    const next = currentIndex < allSections.length - 1 ? allSections[currentIndex + 1] : null;

    return { prev, next };
  };

  const { prev, next } = getNavigationInfo();

  const handleNavigate = (section) => {
    if (!section) return;
    
    if (section.parentId) {
      setActiveTopMenuId(section.parentId);
      setActiveSubItemId(section.id);
    } else {
      setActiveTopMenuId(section.id);
      setActiveSubItemId(null);
    }

    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const currentSectionId = getCurrentSectionId();
  
  // Get content blocks based on current view
  let contentBlocks = [];
  if (activeTopMenuId === "relations" && selectedSubject && selectedObject) {
    const relationKey = `${selectedSubject}-${selectedObject}`;
    contentBlocks = RELATIONS_CONTENT[relationKey] || [];
  } else if (currentSectionId) {
    contentBlocks = CONTENT_BLOCKS[currentSectionId] || [];
  }

  const showLeftButton = activeTopMenuId !== "regional" && prev;
  const showRightButton = activeTopMenuId !== "relations" && next;

  return (
    <div className={styles.page}>
      <NavBar
        mode="indicators"
        topMenus={TOP_MENUS}
        activeTopMenuId={activeTopMenuId}
        onTopMenuChange={handleTopMenuChange}
      />

      {activeTopMenuId === "relations" ? (
        <RelationsSubBar onSelectionChange={handleRelationsSelection} />
      ) : (
        activeMenu && activeMenu.submenu && activeMenu.submenu.length > 0 && (
          <SecondarySubBar
            items={activeMenu.submenu}
            activeId={activeSubItemId}
            onSelect={(id) => {
              setActiveSubItemId(id);
              window.scrollTo({ top: 0, behavior: "instant" });
            }}
          />
        )
      )}

      <main className={styles.main}>
        {contentBlocks.length > 0 ? (
          <div className={styles.content}>
            {contentBlocks.map((block) => (
              <ContentBlock
                key={block.id}
                id={block.id}
                title={block.title}
              >
                {block.chartType === 'pie' && block.pieData ? (
                  <PieChart {...block.pieData} />
                ) : block.chartData ? (
                  <LineChart
                    title={block.title}
                    labels={block.chartData.labels}
                    datasets={block.chartData.datasets}
                  />
                ) : null}
              </ContentBlock>
            ))}
          </div>
        ) : (
          <section className={styles.placeholder}>
            <p>
                "Выберите показатель субъект и показатель объект для просмотра взаимосвязей"
            </p>
          </section>
        )}
      </main>

      {contentBlocks.length > 0 && (
        <PageNavigationMenu blocks={contentBlocks} />
      )}

      <div className={styles.navigationButtons}>
        {showLeftButton && (
          <NavigationButton
            direction="left"
            label={prev.label}
            onClick={() => handleNavigate(prev)}
          />
        )}
        
        {showRightButton && (
          <NavigationButton
            direction="right"
            label={next.label}
            onClick={() => handleNavigate(next)}
          />
        )}
      </div>
    </div>
  );
}
