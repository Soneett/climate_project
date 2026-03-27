import React, { useState, useRef, useEffect, useLayoutEffect, useCallback } from "react";
import { createPortal } from "react-dom";
import { useKeyPress } from "../../hooks/useKeyPress";
import styles from "./Dropdown.module.scss";

export default function Dropdown({ 
  trigger, 
  children, 
  open: controlledOpen, 
  onOpenChange 
}) {
  const [internalOpen, setInternalOpen] = useState(false);
  const rootRef = useRef(null);
  const panelRef = useRef(null);
  const [panelStyle, setPanelStyle] = useState({});
  
  const isControlled = controlledOpen !== undefined;
  const open = isControlled ? controlledOpen : internalOpen;
  
  const setOpen = useCallback((value) => {
    if (isControlled) {
      onOpenChange?.(value);
    } else {
      setInternalOpen(value);
    }
  }, [isControlled, onOpenChange]);

  useEffect(() => {
    function handleClickOutside(event) {
      const inRoot = rootRef.current?.contains(event.target);
      const inPanel = panelRef.current?.contains(event.target);
      if (!inRoot && !inPanel) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [setOpen]);

  useKeyPress("Escape", () => setOpen(false));

  useLayoutEffect(() => {
    if (open && rootRef.current) {
      const rect = rootRef.current.getBoundingClientRect();
      setPanelStyle({
        top: rect.bottom + 8,
        left: rect.left,
      });
    }
  }, [open]);

  return (
    <div className={styles.root} ref={rootRef}>
      <div onClick={() => setOpen(!open)}>
        {trigger}
      </div>
      {open && createPortal(
        <div className={styles.panel} style={panelStyle} ref={panelRef}>
          {children}
        </div>,
        document.body
      )}
    </div>
  );
}
