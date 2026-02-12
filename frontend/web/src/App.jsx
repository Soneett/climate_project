import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import RegionContextProvider from "./context/RegionContextProvider";
import ErrorBoundary from "./components/ErrorBoundary/ErrorBoundary";
import HomePage from "./pages/HomePage/HomePage";
import ComparePage from "./pages/ComparePage/ComparePage";
import RegionIndicatorsPage from "./pages/RegionIndicatorsPage/RegionIndicatorsPage";
import Layout from "./shared/Layout/Layout";

const App = () => {
  return (
    <ErrorBoundary>
      <RegionContextProvider>
        <Router>
          <Routes>
            <Route path="/" element={
              <Layout>
                <HomePage />
              </Layout>
            } />
            <Route path="/compare" element={<ComparePage />} />
            <Route path="/indicators" element={<RegionIndicatorsPage />} />
            <Route path="*" element={
              <Layout>
                <HomePage />
              </Layout>
            } />
          </Routes>
        </Router>
      </RegionContextProvider>
    </ErrorBoundary>
  );
}

export default App
