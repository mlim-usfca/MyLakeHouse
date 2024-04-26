import React, { useState, useEffect } from 'react';
import {
  Box, Typography, Table, TableBody, TableCell, TableHead, TableRow, TableContainer,
  Paper, Button, Collapse, TablePagination
} from '@mui/material';

export const DataFilesTable = ({ database, table }) => {
  const [dataFiles, setDataFiles] = useState([]);
  const [currentPage, setCurrentPage] = useState(1); // Start with page 1
  const [open, setOpen] = useState(false);
  const [isNextPageAvailable, setIsNextPageAvailable] = useState(true); // State to track if next page is available
  const rowsPerPage = 5; // Fixed number of rows per page

  useEffect(() => {
    const fetchDataFiles = async () => {
      try {
        const offset = (currentPage - 1) * rowsPerPage;
        const response = await fetch(`http://localhost:8090/metadata/getDataFiles?db_name=${database}&table_name=${table}&limit=${rowsPerPage}&offset=${offset}`);
        const data = await response.json();
        setDataFiles(data);
        // Check if the next page is available
        setIsNextPageAvailable(data.length === rowsPerPage);
      } catch (error) {
        console.error('Error fetching data files:', error);
      }
    };

    fetchDataFiles();
  }, [currentPage, database, table]);

  const handleChangePage = (event, newPage) => {
    setCurrentPage(newPage + 1); // Adjust because TablePagination is zero-indexed
  };

  return (
    <Box sx={{ marginBottom: 4 }}>
        <Box sx={{ display: 'flex', flexDirection: 'row', alignItems: 'flex-start', gap: 2, justifyContent: 'space-between' }}>
            <Typography variant="h5" gutterBottom>
                Data File Paths
            </Typography>
            <Button onClick={() => setOpen(!open)} variant="contained" sx={{ marginBottom: 2 }}>
                {open ? 'Hide Details' : 'Show Details'}
            </Button>
        </Box>
        <Collapse in={open} timeout="auto" unmountOnExit>
            <TableContainer component={Paper} sx={{ backgroundColor: 'transparent', width: '100%', padding: '16px', maxHeight: '400px', scrollBehavior: 'smooth' }}>
              <Table aria-label="data files table">
                <TableHead>
                  <TableRow>
                    <TableCell>File Path</TableCell>
                    <TableCell align="right">File Size (Bytes)</TableCell>
                    <TableCell align="right">Format</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {dataFiles.map((file, index) => (
                    <TableRow key={index}>
                      <TableCell>{file.file_path}</TableCell>
                      <TableCell align="right">{file.file_size_in_bytes}</TableCell>
                      <TableCell align="right">{file.file_format}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
            <TablePagination
              component="div"
              count={-1} // Unknown total count
              rowsPerPage={rowsPerPage}
              page={currentPage - 1} // Adjust page index for zero-indexed TablePagination
              onPageChange={handleChangePage}
              rowsPerPageOptions={[5]} // Optionally can be removed since rows per page is fixed
              nextIconButtonProps={{ disabled: !isNextPageAvailable }} // Disable the next button if no more pages are available
            />
        </Collapse>
    </Box>
  );
};

