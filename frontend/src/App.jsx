import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import MainView from "./Views/MainView";
import AuthView from "./Views/AuthView"; // Create this new component for Login and Sign-up
import MatchesView from "./Views/MatchesView"; // Add the Matches view
import Header from "./Components/header/Header";
import "./index.css";
import { useLocation } from "react-router-dom";
import React, { useEffect } from "react";

function App() {
  const location = useLocation();

  useEffect(() => {
    if (location.pathname === "/") {
      // MainView: Disable horizontal overflow
      document.body.style.overflow = "hidden";
    } else if (location.pathname === "/auth") {
      // AuthView: Enable vertical scrolling, restrict horizontal scrolling
      document.body.style.overflowX = "hidden";
      document.body.style.overflowY = "auto";
    }
  }, [location]);

  return (
    <div className="App">
      <Header />
      <Routes>
        <Route path="/" element={<MainView className="MainView" />} />
        <Route path="/auth" element={<AuthView className="AuthView" />} />
        <Route path="/matches" element={<MatchesView className="MatchesView" />} /> {/* Add this route */}
      </Routes>
    </div>
  );
}

// Wrap the entire App in a Router
export default function AppWithRouter() {
  return (
    <Router>
      <App />
    </Router>
  );
}
