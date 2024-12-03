import React from 'react';
import { Favorite } from '@mui/icons-material';
import { IconButton } from '@mui/material';

const HeartButton = ({ onClick }) => {
  return (
    <IconButton onClick={onClick} sx={{ color: "lightgreen" }} size="large">
      <Favorite fontSize='large'/>
    </IconButton>
  );
}

export default HeartButton;