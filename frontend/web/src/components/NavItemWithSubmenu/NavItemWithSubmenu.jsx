import React, {useState, useRef, useEffect} from "react";
import styles from "./NavItemWithSubmenu.module.scss";

const NavItemWithSubmenu = (
  {
    id, label, submenu = [],
    isActive = false,
    onActivate = () => {},
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
      className={`${styles.root} ${open ? styles.open : ""}`}
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
        <span className={styles.caret} aria-hidden>{open ? "▴" : "▾"}</span>
      </div>
    </div>
  );
}

export default NavItemWithSubmenu
