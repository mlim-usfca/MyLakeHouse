import React from 'react';
import Box from '@mui/material/Box';

export const SparkPerformance = () => {
    return (
        <Box sx={{ width: '100%', height: '100%' }}>
            <iframe
                src="http://localhost:3001/d/ddkn6773qomwwf/sql-query-duration?orgId=1&from=1714782930603&to=1714783830603&viewPanel=1"
                frameBorder="0"
                width="100%"
                height="100%"
            ></iframe>
        </Box>
    );
};