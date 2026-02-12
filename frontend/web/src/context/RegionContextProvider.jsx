import React, { useState, useCallback } from "react";
import { RegionContext } from "./RegionContext";
import { REGIONS } from "../constants/regions";

const RegionContextProvider = ({ children }) => {
  const [region, setRegionState] = useState("Республика Алтай");
  const [error, setError] = useState(null);

  const setRegion = useCallback((newRegion) => {
    // Validate region
    if (!REGIONS.includes(newRegion)) {
      const errorMsg = `Недопустимый регион: ${newRegion}. Допустимые регионы: ${REGIONS.join(", ")}`;
      setError(errorMsg);
      console.error(errorMsg);
      return false;
    }
    
    setError(null);
    setRegionState(newRegion);
    return true;
  }, []);

  const value = {
    region,
    setRegion,
    error,
    availableRegions: REGIONS,
  };

  return (
    <RegionContext.Provider value={value}>
      {children}
    </RegionContext.Provider>
  );
};

export default RegionContextProvider;
