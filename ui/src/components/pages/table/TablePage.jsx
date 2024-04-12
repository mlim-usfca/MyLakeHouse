import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Box, Typography, CircularProgress } from '@mui/material';
import axios from 'axios';

export const TablePage = () => {
  const { database, table } = useParams();
  const [tableInfo, setTableInfo] = useState({});

  useEffect(() => {
    fetchTableInfo(database, table);
  }, [database, table]);

  const fetchTableInfo = async (database, table ) => {
    try {
      console.log(table);
      const response = await axios.get(`http://localhost:8090/props/getTableProps?db_name=${database}&table_name=${table}`)
      console.log(response.data);
      setTableInfo(response.data); // Update table list state)
    } catch (error) {
      console.error('Error fetching table list:', error);
    }
  };


  return (
    <Box sx={{ width: '100%', padding: 2 }}>
      <Typography className="glass-text" variant="subtitle2" align="right" sx={{ fontSize: 24, marginBottom: 4 }}>
        {table} in {database}
      </Typography>
  
      {/* Display table summary information */}
      <Box sx={{ marginBottom: 4 }}>
        {Object.entries(tableInfo).map(([key, value]) => (
          <Typography key={key} variant="body1" gutterBottom>
            {key}: {value}
          </Typography>
        ))}
      </Box>

      <Box sx={{ width: '100%', borderBottom: '1px solid', marginBottom: 4 }} />
  
      {/* Links to snapshots and table properties */}
      <Box sx={{ display: 'flex', flexDirection: 'column' }}>
        <Typography variant="body1" component="p" sx={{ marginBottom: 2 }}>
          <Link to={`/snapshot/${database}/${table}`}>View Snapshots</Link>
        </Typography>
        <Typography variant="body1" component="p">
          <Link to={`/${database}/${table}/properties`}>View Table Properties</Link>
        </Typography>
      </Box>
    </Box>
  );
  
};
