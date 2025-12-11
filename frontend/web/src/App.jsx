import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { RegionContext } from "./context/RegionContext";
import RootWithNav from "./components/RootWithNav/RootWithNav.jsx";
import ComparePage from "./components/ComparePage/ComparePage.jsx";
import RegionIndicatorsPage from "./components/RegionIndicatorsPage/RegionIndicatorsPage.jsx";

const App = () => {
  const [region, setRegion] = useState("Республика Алтай");

  return (
    <RegionContext.Provider value={{ region, setRegion }}>
      <Router>
        <Routes>
          <Route path="/" element={<RootWithNav />} />
          <Route path="/compare" element={<ComparePage />} />
          <Route path="/indicators" element={<RegionIndicatorsPage />} />
          <Route path="*" element={<RootWithNav />} />
        </Routes>
      </Router>
    </RegionContext.Provider>
  );
}

export default App