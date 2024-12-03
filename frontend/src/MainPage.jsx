import React, { useState } from "react";
import "./MainPage.css";
import 'bootstrap/dist/css/bootstrap.min.css';
import CloseButton from "./Components/CloseButton";
import HeartButton from "./Components/HeartButton";
import AccountButton from "./Components/AccountButton";
import DarkModeButton from "./Components/DarkmodeButton";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

const MainPage = () => {
  const [darkMode, setDarkMode] = useState(false);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  return (
    <div className={`main-page ${darkMode ? "dark" : "light"}`}>
      <Container fluid className="h-100 d-flex flex-column">
        {/* Top Row: Account and Dark Mode Buttons */}
        <Row className="mb-3 flex-shrink-0">
          <Col xs={6} className="account-button top-buttons">
            <AccountButton/>
          </Col>
          <Col xs={6} className="darkmode-button top-buttons">
            <DarkModeButton onClick={toggleDarkMode} isDarkMode={darkMode} />
          </Col>
        </Row>

        {/* Middle Row: Swiping Card Placeholder */}
        <Row className="flex-grow-1 d-flex justify-content-center align-items-center">
          <Col className="d-flex justify-content-center">
            <h1 className="swiping-cards-placeholder">Card</h1> {/* Replace this with your swiping card component */}
          </Col>
        </Row>

        {/* Bottom Row: Close and Heart Buttons */}
        <Row className="mb-3 flex-shrink-0">
          <Col xs={6} className="bottom-buttons">
            <CloseButton />
          </Col>
          <Col xs={6} className="bottom-buttons">
            <HeartButton />
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default MainPage;