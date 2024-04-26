import {React, useState, useEffect} from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper,  Box, Typography, Button} from '@mui/material';
import axios from 'axios';
import { snapshotDetail } from '../../../../public/testdata.js';

export const SnapshotDetail = () => {
  const { database, table, id } = useParams();
  const snapshotData = snapshotDetail;
  // Mock data, replace this with your actual fetch logic

  const navigate = useNavigate();

  const handleDeleteSnapshot = async () => {
    try {
      const response = await axios.delete(`http://your-api-url/snapshots/${id}`);
      console.log(response.data);
      alert('Snapshot deleted successfully');
      navigate('/');  // Adjust this to your needs, such as going back to the listing page
    } catch (error) {
      console.error('Failed to delete snapshot:', error);
      alert('Failed to delete snapshot');
    }
  };

  // Generate rows for the summary section
  const summaryRows = Object.entries(snapshotData.summary).map(([key, value]) => (
    <TableRow key={key}>
      <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}} component="th" scope="row">{key}</TableCell>
      <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}} align="right">{value}</TableCell>
    </TableRow>
  ));

  return (
    <Box sx={{width: '100%', padding: 2}}>
      <Typography className="glass-text" variant="subtitle2" align="right" >
        Snapshot {id}
      </Typography>
      <Typography className="glass-text" variant="subtitle2" align="right"
                                sx={{fontSize: 24, marginBottom: 4}}>
        {database} / {table}
      </Typography>
      <TableContainer component={Paper} sx={{backgroundColor: 'transparent', width: '100%',
            padding: '16px',
            maxHeight: '550px',
            scrollBehavior: 'smooth'}}>
        <Table aria-label="Snapshot Details">
          <TableHead>
            <TableRow>
              <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}}>Attribute</TableCell>
              <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}} align="right">Value</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            <TableRow>
              <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}} component="th" scope="row">Made Current At</TableCell>
              <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}} align="right">{snapshotData.made_current_at}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}} component="th" scope="row">Snapshot ID</TableCell>
              <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}} align="right">{snapshotData.snapshot_id}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}} component="th" scope="row">Is Current Ancestor</TableCell>
              <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}} align="right">{snapshotData.is_current_ancestor}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}} component="th" scope="row">Committed At</TableCell>
              <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}} align="right">{snapshotData.committed_at}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}} component="th" scope="row">Operation</TableCell>
              <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}} align="right">{snapshotData.operation}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}} component="th" scope="row">Manifest List</TableCell>
              <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}} align="right">{snapshotData.manifest_list}</TableCell>
            </TableRow>
            {/* Render the summary in a separate section or as part of the main table */}
            {summaryRows}
          </TableBody>
        </Table>
      </TableContainer>
      <Button
        variant="contained"
        color="error"
        onClick={() => handleDeleteSnapshot(id)}
        sx={{ marginTop: 2, display: 'block' }}
      >
        Delete Snapshot
    </Button>
    </Box>
  );
};