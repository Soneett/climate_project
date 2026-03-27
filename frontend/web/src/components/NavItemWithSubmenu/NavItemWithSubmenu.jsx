import React, {useState, useRef, useEffect} from "react";
import styles from "./NavItemWithSubmenu.module.scss";

const NavItemWithSubmenu = (
  {
    id: _id, label, submenu = [],
    isActive = false,
    onActivate = () => {},
    onSubmenuItemSelect = () => {},
  }) => {

  const [open, setOpen] = useState(isActive);
  const rootRef = useRef(null);

  useEffect(() => setOpen(isActive), [isActive]);

  useEffect(() => {
    function onClickOutside(event) {
      if (rootRef.current && !rootRef.current.contains(event.target)) {
        setOpen(false);
        onActivate(false);
      }
    }

    function onEsc(event) {
      if (event.key === "Escape") {
        setOpen(false);
        onActivate(false);
      }
    }

    document.addEventListener("mousedown", onClickOutside);
    document.addEventListener("keydown", onEsc);
    return () => {
      document.removeEventListener("mousedown", onClickOutside);
      document.removeEventListener("keydown", onEsc);
    };
  }, [onActivate]);

  function handleToggle() {
    const next = !open;
    setOpen(next);
    onActivate(next);
  }

  return (
    <div
      className={`${styles.root} ${open ? styles.open : ""} ${isActive ? styles.active : ""}`}
      ref={rootRef}
    >
      <div
        className={`${styles.trigger}`}
        onClick={handleToggle}
        onKeyDown={(e) => {
          if (e.key === "Enter") handleToggle();
        }}
        role="button"
        tabIndex={0}
        aria-expanded={open}
        aria-haspopup={submenu.length > 0 ? "true" : "false"}
      >
        <span className={styles.label}>
          {label.split("\n").map((line, i) => <span key={i} className={styles.line}>{line}</span>)}
        </span>
      </div>
      {open && submenu.length > 0 && (
        <ul className={styles.submenu} role="menu">
          {submenu.map((item) => (
            <li
              key={item.id}
              className={styles.submenuItem}
              role="menuitem"
              tabIndex={0}
              onClick={() => { onSubmenuItemSelect(item); setOpen(false); onActivate(false); }}
              onKeyDown={(e) => {
                if (e.key === "Enter" || e.key === " ") {
                  e.preventDefault();
                  onSubmenuItemSelect(item);
                  setOpen(false);
                  onActivate(false);
                }
              }}
            >
              {item.label}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default NavItemWithSubmenu
