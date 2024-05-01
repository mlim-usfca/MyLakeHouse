import React from 'react';
import Box from '@mui/material/Box';

export const SparkPerformance = () => {
    return (
        <Box sx={{ width: '100%', height: '100%' }}>
            <iframe
                src="http://localhost:3001/public-dashboards/e3259924ddb34edabc96258a890e1ab5"
                frameBorder="0"
                width="100%"
                height="100%"
                allowTransparency
            ></iframe>
        </Box>
    );
};