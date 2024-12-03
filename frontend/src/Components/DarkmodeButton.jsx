import React from 'react';
import { WbSunny, Nightlight } from '@mui/icons-material';
import { IconButton } from '@mui/material';

const DarkModeButton = ({ onClick, isDarkMode }) => {
  return (
    <IconButton onClick={onClick} sx={{ color: "grey" }} size="large">
      {isDarkMode ? <WbSunny fontSize="large" /> : <Nightlight fontSize="large" />}
    </IconButton>
  );
}

export default DarkModeButton;