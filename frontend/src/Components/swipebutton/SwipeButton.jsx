import React from 'react';
import './swipebuttons.css';
import { Close, Favorite } from '@mui/icons-material';
import { IconButton } from '@mui/material';

function SwipeButton({ onSwipeLeft, onSwipeRight }) {
    return (
        <div className="SwipeButtons">
            <IconButton className="SwipeButtons__left" onClick={onSwipeLeft}>
                <Close fontSize="large" />
            </IconButton>
            <IconButton className="SwipeButtons__right" onClick={onSwipeRight}>
                <Favorite fontSize="large" />
            </IconButton>
        </div>
    );
}

export default SwipeButton;