import React from 'react';
import { Person } from '@mui/icons-material';
import { IconButton } from '@mui/material';

const AccountButton = ({ onClick }) => {
  return (
    <IconButton onClick={onClick} sx={{ color: "grey" }} size="large" >
      <Person fontSize='large'/>
    </IconButton>
  );
}

export default AccountButton;