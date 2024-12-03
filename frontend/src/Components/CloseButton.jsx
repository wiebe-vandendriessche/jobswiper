import React from 'react';
import { Close } from '@mui/icons-material';
import { IconButton } from '@mui/material';

const CloseButton = ({ onClick }) => {
  return (
    <IconButton onClick={onClick} sx={{ color: "pink" }} size="large" className='SwipeButtons'>
      <Close fontSize='large'/>
    </IconButton>
  );
}

export default CloseButton;