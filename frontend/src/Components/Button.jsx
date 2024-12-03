import React from 'react';

import { Button  } from '@mui/material';

function Button(props) {
    return (
        <div className="SwipeButtons">
            <Button>
                {props.children}
            </Button>
        </div>
    );
}

export default Button;