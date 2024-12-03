import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import MainView from "./Views/MainView";
import AuthView from "./Views/AuthView"; // Create this new component for Login and Sign-up

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainView />} />
        <Route path="/auth" element={<AuthView />} />
      </Routes>
    </Router>
  );
}

export default App;
