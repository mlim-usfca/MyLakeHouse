import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { Box, Typography } from '@mui/material';

export const TablePage = () => {
  const { database, table } = useParams();


  return (
    <Box sx={{ width: '100%', typography: 'body1' }}>
      <Typography variant="p" component="p" sx={{ textAlign: 'left' }}>
        Summary Information for {table} in {database}
      </Typography>
      {/* Display table summary information */}
      <Typography variant="body1" component="p">
        {/* Display relevant table info, such as number of rows, columns, etc. */}
        {/* Example: Number of rows: {tableInfo.rows}, Number of columns: {tableInfo.columns} */}
      </Typography>
      {/* Links to snapshots and table properties */}
      <Typography variant="body1" component="p">
        <Link to={`/snapshot/${database}/${table}`}>View Snapshots</Link>
      </Typography>
      <Typography variant="body1" component="p">
        <Link to={`/tableproperties/${database}/${table}`}>View Table Properties</Link>
      </Typography>
    </Box>
  );
};
