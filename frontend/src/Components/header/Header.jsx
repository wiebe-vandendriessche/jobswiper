import React from "react";
import { Person } from '@mui/icons-material';
import { IconButton } from '@mui/material';
import { Forum } from '@mui/icons-material';
import { useNavigate } from "react-router-dom";
import { Button } from '@mui/material';

import "./header.css";

function Header() {
  const navigate = useNavigate();

  const handlePersonClick = () => {
    navigate("/auth"); // Navigate to the auth route
  };

  const handleHomeClick = () => {
    navigate("/"); // Navigate to the home route
  };

  const handleForumClick = () => {
    navigate("/matches"); // Navigate to the matches route
  };

  return (
    <div className="header">
      <IconButton onClick={handlePersonClick}>
        <Person fontSize="large" className="header__icon" />
      </IconButton>
      <div onClick={handleHomeClick} className="header__logo">
        <Button color="black">
          <h1>Job Finder</h1>
        </Button>
      </div>
      <IconButton onClick={handleForumClick}>
        <Forum fontSize="large" className="header__icon" />
      </IconButton>
    </div>
  );
}

export default Header;
