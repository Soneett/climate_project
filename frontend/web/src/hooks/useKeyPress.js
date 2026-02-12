import { useEffect } from "react";

export function useKeyPress(targetKey, handler) {
  useEffect(() => {
    const listener = (event) => {
      if (event.key === targetKey) handler(event);
    };
    document.addEventListener("keydown", listener);
    return () => document.removeEventListener("keydown", listener);
  }, [targetKey, handler]);
}
