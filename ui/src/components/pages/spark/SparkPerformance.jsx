import React from 'react';
import Box from '@mui/material/Box';

export const SparkPerformance = () => {
    return (
        <Box sx={{ width: '100%', height: '100%' }}>
            <iframe
                src="http://localhost:3001/dashboard/new?orgId=1&from=1714729957497&to=1714751557497&viewPanel=1"
                frameBorder="0"
                width="100%"
                height="100%"
            ></iframe>
        </Box>
    );
};