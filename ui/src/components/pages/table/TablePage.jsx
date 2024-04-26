import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Box, Typography, Table, TableBody, TableCell, TableHead, TableRow, TableContainer,Paper} from '@mui/material';
import { fetchData } from '@/services/table/service';
import { DataFilesTable } from './DataFiles';

export const TablePage = () => {
  const { database, table } = useParams();
  const [tableInfo, setTableInfo] = useState({});
  const [schema, setSchema] = useState([]);

  useEffect(() => {
    fetchTableInfo(database, table);
  }, [database, table]);

  const fetchTableInfo = async (database, table ) => {
    try {
      console.log(table);
      const { tableInfoData, schemaData } = await fetchData(database, table);
      setTableInfo(tableInfoData);
      setSchema(schemaData); 
    } catch (error) {
      console.error('Error fetching table info:', error);
    }
  };


  return (
    <Box sx={{ width: '100%', paddingLeft: 4, paddingRight: 4 }}>
      <Typography className="glass-text" variant="subtitle2" align="right" sx={{ fontSize: 24, marginBottom: 4 }}>
          {table} in {database}
      </Typography>
      <Box sx={{ width: '100%', display: 'flex', flexDirection: 'row', alignItems: 'flex-start', justifyContent: 'space-between'}}>

    
        {/* Display table summary information */}
        <Box sx={{ marginBottom: 4 }}>
          <Typography variant="h5" gutterBottom>
                    Table Info
          </Typography>
          {Object.entries(tableInfo).map(([key, value]) => (
            <Typography key={key} variant="body1" gutterBottom>
              {key}: {value}
            </Typography>
          ))}
        </Box>

        <Box sx={{ marginBottom: 4 }}>
        <Typography variant="h5" gutterBottom>
                    Table Schema
          </Typography>
          <TableContainer component={Paper} sx={{backgroundColor: 'transparent', width: '100%',
              padding: '16px',
              maxHeight: '400px',
              scrollBehavior: 'smooth'}}>
            <Table aria-label="schema table">
              <TableHead>
                <TableRow>
                  <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}}>Column Name</TableCell>
                  <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}}>Type</TableCell>
                  <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}}>Nullable</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {schema.map((column, index) => (
                  <TableRow key={index}>
                    <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}}>{column.name}</TableCell>
                    <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}}>{column.type}</TableCell>
                    <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}}>{column.nullable ? 'Yes' : 'No'}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Box>
      </Box>

      <Box sx={{ width: '100%', borderBottom: '1px solid', marginBottom: 4 }} />
      <DataFilesTable
        database={database}
        table={table}
      />
  
      {/* Links to snapshots and table properties */}
      <Box sx={{ display: 'flex',flexDirection: 'row', alignItems: 'flex-start', gap: 2  }}>
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
