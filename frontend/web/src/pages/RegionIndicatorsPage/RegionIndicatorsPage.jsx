import React, { useState, useEffect, useContext } from "react";
import NavBar from "../../components/NavBar/NavBar";
import SecondarySubBar from "../../components/SecondarySubBar/SecondarySubBar";
import RelationsSubBar from "../../components/RelationsSubBar/RelationsSubBar";
import ContentBlock from "../../components/ContentBlock/ContentBlock";
import ChartRenderer from "../../components/Charts/ChartRenderer";
import NavigationButton from "../../components/NavigationButton/NavigationButton";
import PageNavigationMenu from "../../components/PageNavigationMenu/PageNavigationMenu";
import { useContentData } from "../../hooks/useContentData";
import { TOP_MENUS } from "../../constants/navigationMenus";
import { RegionContext } from "../../context/RegionContext";
import styles from "./RegionIndicatorsPage.module.scss";

export default function RegionIndicatorsPage() {
  const {
    contentBlocks: CONTENT_BLOCKS,
    relationsContentBlocks: RELATIONS_CONTENT,
    hasData: regionHasData,
    loading
  } = useContentData();

  const { region } = useContext(RegionContext);

  const [activeTopMenuId, setActiveTopMenuId] = useState(null);
  const [activeSubItemId, setActiveSubItemId] = useState(null);
  const [selectedSubject, setSelectedSubject] = useState(null);
  const [selectedObject, setSelectedObject] = useState(null);

  const activeMenu = TOP_MENUS.find(m => m.id === activeTopMenuId);

  useEffect(() => {
    const defaultTop = TOP_MENUS.find(m => m.id === "regional") || TOP_MENUS[0];
    setActiveTopMenuId(defaultTop.id);
    if (defaultTop.submenu && defaultTop.submenu.length > 0) {
      setActiveSubItemId(defaultTop.submenu[0].id);
    }
  }, []);

  const handleTopMenuChange = (newId) => {
    if (!newId) return;
    setActiveTopMenuId(newId);
    const menu = TOP_MENUS.find(m => m.id === newId);
    if (menu.submenu && menu.submenu.length > 0) {
      setActiveSubItemId(menu.submenu[0].id);
    } else {
      setActiveSubItemId(null);
    }

    setSelectedSubject(null);
    setSelectedObject(null);

    window.scrollTo({ top: 0, behavior: "instant" });
  };

  const handleRelationsSelection = (subjectId, objectId) => {
    setSelectedSubject(subjectId);
    setSelectedObject(objectId);

    window.scrollTo({ top: 0, behavior: "instant" });
  };

  const getCurrentSectionId = () => {
    if (activeSubItemId) return activeSubItemId;
    if (activeTopMenuId) return activeTopMenuId;
    return null;
  };

  const getNavigationInfo = () => {
    const currentSectionId = getCurrentSectionId();
    if (!currentSectionId) return { prev: null, next: null };

    const allSections = [];
    TOP_MENUS.forEach(menu => {
      if (menu.submenu && menu.submenu.length > 0) {
        menu.submenu.forEach(sub => {
          allSections.push({ id: sub.id, label: sub.label, parentId: menu.id });
        });
      } else {
        allSections.push({ id: menu.id, label: menu.label.replace(/\n/g, " "), parentId: null });
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


  let contentBlocks = [];
  if (activeTopMenuId === "relations" && selectedSubject && selectedObject) {
    const relationKey = `${selectedSubject}-${selectedObject}`;
    contentBlocks = RELATIONS_CONTENT[relationKey] || [];
  } else if (currentSectionId) {
    contentBlocks = CONTENT_BLOCKS[currentSectionId] || [];
  }

  const showLeftButton = activeTopMenuId !== "regional" && prev;
  const showRightButton = activeTopMenuId !== "relations" && next;

  if (loading) {
    return (
      <div className={styles.page}>
        <div className={styles.loading}>Загрузка данных...</div>
      </div>
    );
  }

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
        {!regionHasData ? (
          <section className={styles.placeholder}>
            <p>Данные для региона «{region}» пока не доступны</p>
          </section>
        ) : contentBlocks.length > 0 ? (
          <div className={styles.content}>
            {contentBlocks.map((block) => (
              <ContentBlock
                key={block.id}
                id={block.id}
                title={block.title}
              >
                <ChartRenderer block={block} />
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

      {regionHasData && contentBlocks.length > 0 && (
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
