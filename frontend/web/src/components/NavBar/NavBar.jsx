import React from "react";
import styles from "./NavBar.module.scss";
import CompareDropdown from "../../shared/CompareDropdown/CompareDropdown";
import ChangeRegionDropdown from "../../shared/ChangeRegionDropdown/ChangeRegionDropdown";
import NavItemWithSubmenu from "../NavItemWithSubmenu/NavItemWithSubmenu";
import {useNavigate} from "react-router-dom";

const NavBar = ({
                  mode = "default",
                  topMenus = [],
                  activeTopMenuId = null,
                  onTopMenuChange = () => {}
                }) => {
  const navigate = useNavigate();

  if (mode === "indicators") {
    return (
      <header className={styles.header} role="banner">
        <div className={styles.inner}>
          <div
            className={styles.brand}
            role="button"
            tabIndex={0}
            onClick={() => navigate("/")}
            onKeyDown={(e) => {
              if (e.key === "Enter") navigate("/");
            }}
            aria-label="Перейти на главную"
          >
            Лаборатория урбанистических<br/>исследований ВШЭ
          </div>

          <nav
            className={styles.controls} aria-label="Показатели - навигация">
            {topMenus.map((indicatorsSection) => (
              <div key={indicatorsSection.id} className={`${styles.item} ${indicatorsSection.submenu?.length ? 'has-submenu' : ''}`}>
                <NavItemWithSubmenu
                  id={indicatorsSection.id}
                  label={indicatorsSection.label}
                  submenu={indicatorsSection.submenu}
                  isActive={activeTopMenuId === indicatorsSection.id}
                  onActivate={(open) => onTopMenuChange(open ? indicatorsSection.id : null)}
                />
              </div>
            ))}
          </nav>
        </div>
      </header>
    );
  }
  return (
    <header className={styles.header} role="banner">
      <div className={styles.inner}>
        <div 
          className={styles.brand}
          role="button"
          tabIndex={0}
          onClick={() => navigate("/")}
          onKeyDown={(e) => {
            if (e.key === "Enter") navigate("/");
          }}
          aria-label="Перейти на главную"
        >
          Лаборатория урбанистических исследований ВШЭ
        </div>

        <nav className={styles.controls} aria-label="Главная навигация">
          <div className={styles.item}>
            <CompareDropdown/>
          </div>

          <div className={styles.item}>
            <ChangeRegionDropdown/>
          </div>

          <div className={styles.itemRight}
               role="button"
               tabIndex={0}
               onClick={() => navigate("/indicators")}
               onKeyDown={(e) => {
                 if (e.key === "Enter") navigate("/indicators");
               }}>
            <span className={styles.btn}>Показатели региона</span>
          </div>
        </nav>
      </div>
    </header>
  );
};

export default NavBar;
