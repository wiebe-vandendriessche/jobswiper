import React from "react";
import { Person } from '@mui/icons-material';
import { IconButton } from '@mui/material';
import { Forum } from '@mui/icons-material';
import { useNavigate } from "react-router-dom";

import "./header.css";

function Header(props) {
  const navigate = useNavigate();

  const handlePersonClick = () => {
    navigate("/auth"); // Navigate to the auth route
  };
  
  return (
    <div className="header">
      <IconButton onClick={handlePersonClick}>
        <Person fontSize="large" className="header__icon" />
      </IconButton>
      <h1>
        Job Finder
      </h1>
      <IconButton>
        <Forum fontSize="large" className="header__icon" />
      </IconButton>
    </div>
  );
}

export default Header;
