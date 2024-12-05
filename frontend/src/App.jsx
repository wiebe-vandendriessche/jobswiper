import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import MainView from "./Views/MainView";
import AuthView from "./Views/AuthView"; // Create this new component for Login and Sign-up
import Header from "./Components/header/Header";
import "./index.css";

function App() {
  return (
    <>
      <Router>
        <div className="App">
          <Header />
          <Routes>
            <Route path="/" element={<MainView />} />
            <Route path="/auth" element={<AuthView />} />
          </Routes>
        </div>
      </Router >
    </>
  );
}

export default App;
