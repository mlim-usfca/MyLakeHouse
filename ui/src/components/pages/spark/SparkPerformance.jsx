import React from 'react';
import Box from '@mui/material/Box';

export const SparkPerformance = () => {
    return (
        <Box sx={{ width: '100%', height: '100%' }}>
            <iframe
                src={`${import.meta.env.VITE_HOST}:${import.meta.env.VITE_GRAFANA_PORT}`}
                frameBorder="0"
                width="100%"
                height="100%"
            ></iframe>
        </Box>
    );
};