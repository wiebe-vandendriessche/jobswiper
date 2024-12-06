import React from 'react';
import './swipebuttons.css';
import { Replay } from '@mui/icons-material';
import { Close } from '@mui/icons-material';
import { StarRate } from '@mui/icons-material';
import { Favorite } from '@mui/icons-material';
import { FlashOn } from '@mui/icons-material';
import { IconButton } from '@mui/material';

function SwipeButton(props) {
    return (
        <div className="SwipeButtons">
            <IconButton className="SwipeButtons__left">
            <Close fontSize="large" />
            </IconButton>
            <IconButton className="SwipeButtons__right">
            <Favorite fontSize="large" />
            </IconButton>
        </div>
    );
}

export default SwipeButton;