import React, { useState, useEffect } from 'react';
import {
  Box, Typography, Table, TableBody, TableCell, TableHead, TableRow, TableContainer,
  Paper, Button, Collapse, TablePagination
} from '@mui/material';

export const DataFilesTable = ({ database, table, setCollapsed }) => {
  const [dataFiles, setDataFiles] = useState([]);
  const [currentPage, setCurrentPage] = useState(1); // Start with page 1
  const [open, setOpen] = useState(false);
  const [isNextPageAvailable, setIsNextPageAvailable] = useState(true); // State to track if next page is available
  const rowsPerPage = 5; // Fixed number of rows per page

  useEffect(() => {
    const fetchDataFiles = async () => {
      try {
        const offset = (currentPage - 1) * rowsPerPage;
        const response = await fetch(`${import.meta.env.VITE_HOST}:${import.meta.env.VITE_BE_API_PORT}/metadata/getDataFiles?db_name=${database}&table_name=${table}&limit=${rowsPerPage}&offset=${offset}`);
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
    <Box sx={{ marginBottom: 2 }}>
      <Box sx={{ display: 'flex', flexDirection: 'row', alignItems: 'flex-start', gap: 2, justifyContent: 'space-between' }}>
        <Typography fontSize={18} className="glass-text-12" variant="subtitle2" align="left" >
          Data File Paths
        </Typography>
        <Button onClick={() => { setOpen(!open), setCollapsed(open) }} variant="contained" sx={{ marginBottom: 2 }}>
          {open ? 'Hide Details' : 'Show Details'}
        </Button>
      </Box>
      <Collapse in={open} timeout="auto" unmountOnExit>
        <TableContainer component={Paper} sx={{ backgroundColor: 'transparent', width: '100%', padding: '16px', maxHeight: "400", scrollBehavior: 'smooth' }}>
          <Table aria-label="data files table">
            <TableHead>
              <TableRow>
                <TableCell sx={{ borderBottom: "1px solid rgba(0, 0, 0, .1)" }}>File Path</TableCell>
                <TableCell align="right" sx={{ borderBottom: "1px solid rgba(0, 0, 0, .1)" }}>File Size (Bytes)</TableCell>
                <TableCell align="right" sx={{ borderBottom: "1px solid rgba(0, 0, 0, .1)" }}>Format</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {dataFiles.map((file, index) => (
                <TableRow key={index}>
                  <TableCell sx={{ borderBottom: "1px solid rgba(0, 0, 0, .1)" }}>{file.file_path}</TableCell>
                  <TableCell align="right" sx={{ borderBottom: "1px solid rgba(0, 0, 0, .1)" }}>{file.file_size_in_bytes}</TableCell>
                  <TableCell align="right" sx={{ borderBottom: "1px solid rgba(0, 0, 0, .1)" }}>{file.file_format}</TableCell>
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

