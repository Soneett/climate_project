import React, { useState, useRef } from "react";
import { useClickOutside } from "../../hooks/useClickOutside";
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
  
  const isControlled = controlledOpen !== undefined;
  const open = isControlled ? controlledOpen : internalOpen;
  
  const setOpen = (value) => {
    if (isControlled) {
      onOpenChange?.(value);
    } else {
      setInternalOpen(value);
    }
  };

  useClickOutside(rootRef, () => setOpen(false));
  useKeyPress("Escape", () => setOpen(false));

  return (
    <div className={styles.root} ref={rootRef}>
      <div onClick={() => setOpen(!open)}>
        {trigger}
      </div>
      {open && (
        <div className={styles.panel}>
          {children}
        </div>
      )}
    </div>
  );
}
