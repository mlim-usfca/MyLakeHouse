import {React, useState, useEffect} from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper,  Box, Typography, Button} from '@mui/material';
import { deleteSnapshot, getSnapshoData } from '@/services/snapshot/services.js';
import axios from "axios";

export const SnapshotDetail = () => {
  const { database, table, id } = useParams();
  const [snapshotData, setSnapshotData] = useState({summary:{}});
  const [tags, setTags] = useState([]);
  const [branches, setBranches] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getSnapshoData(database, table, id);
        const { snapshots, tags, branches } = data;
        console.log(data);
        setSnapshotData(snapshots[0]);
        setTags(tags);
        setBranches(branches);
      } catch (error) {
        console.error('Error fetching snapshots, tags, and branches:', error);
      }
    };
    fetchData();
  },[database, table,id]);

  const navigate = useNavigate();

  const handleDeleteSnapshot = async () => {
    // Display confirmation dialog
    const confirmDelete = window.confirm('Are you sure you want to delete this snapshot?');
  
    // Check if user confirmed deletion
    if (confirmDelete) {
      try {
        const response = await deleteSnapshot(database, table, id);
        alert('Snapshot deleted successfully');
        navigate(`/snapshot/${database}/${table}`);
      } catch (error) {
        console.error('Failed to delete snapshot:', error);
        alert('Failed to delete snapshot');
      }
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
              <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}} component="th" scope="row">Related Branch</TableCell>
              <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}} align="right">{branches.map((branch, index) => (
    <span key={branch.name}>{branch.name}{index !== branches.length - 1 ? ', ' : ''}</span>))}
            </TableCell>
            </TableRow>
            <TableRow>
              <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}} component="th" scope="row">Related Tags</TableCell>
              <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}} align="right">{tags.map((branch, index) => (
    <span key={branch.name}>{branch.name}{index !== branches.length - 1 ? ', ' : ''}</span>))}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}} component="th" scope="row">Related Branch</TableCell>
              <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}} align="right">{branches.map((branch, index) => (
    <span key={branch.name}>{branch.name}{index !== branches.length - 1 ? ', ' : ''}</span>))}
            </TableCell>
            </TableRow>
            <TableRow>
              <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}} component="th" scope="row">Related Tags</TableCell>
              <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}} align="right">{tags.map((branch, index) => (
    <span key={branch.name}>{branch.name}{index !== branches.length - 1 ? ', ' : ''}</span>))}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}} component="th" scope="row">Snapshot ID</TableCell>
              <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}} align="right">{snapshotData.snapshot_id}</TableCell>
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