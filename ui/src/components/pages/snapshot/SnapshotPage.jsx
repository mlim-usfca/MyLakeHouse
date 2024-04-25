import React, { useState, useEffect, useMemo} from 'react';
import { TreeView } from '@mui/x-tree-view/TreeView';
import { TreeItem } from '@mui/x-tree-view/TreeItem';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import { Tabs, Tab, Box, Typography } from '@mui/material';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { backend } from '@/services/service';

export const SnapshotPage = () => {
  let { database, table } = useParams();

  
  // Provide default values for testing now 
  database = database || 'Test Database';
  table = table || 'Test Table';

  const [tabValue, setTabValue] = useState(0);
  const [snapshots, setSnapshots] = useState([]);
  const [tags, setTags] = useState([]);
  const [branches, setBranches] = useState([]);

  const navigate = useNavigate();

  const handleDoubleClick = (snapshotId) => {
    navigate(`/snapshotDetails/${database}/${table}/${snapshotId}`);
  };

  // Recursive function to render TreeItems
  const renderTree = (nodes) => {
    return nodes.map((node) => (
      <TreeItem
        key={node.snapshot_id}
        nodeId={node.snapshot_id}
        label={`Snapshot ${node.snapshot_id}`}
        onDoubleClick={() => handleDoubleClick(node.snapshot_id)}
      >
        {node.children && renderTree(node.children)}
      </TreeItem>
    ));
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(backend + `dashboard/snapshots?branch_name=main&db_name=${database}&table_name=${table}`);
        const { snapshots, tags, branches } = response.data.response;
        console.log(response.data.response)
        setSnapshots(snapshots);
        setTags(tags);
        setBranches(branches);
      } catch (error) {
        console.error('Error fetching snapshots, tags, and branches:', error);
      }
    };
    fetchData();
  },[database, table]);

  

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const snapshotTree = useMemo(() => {
    const buildSnapshotTree = (snapshots, parentId = undefined) => {
      const children = snapshots.filter(snapshot => snapshot.parent_id === parentId);
      return children.map(child => ({
        ...child,
        children: buildSnapshotTree(snapshots, child.snapshot_id)
      }));
    };

    return buildSnapshotTree(snapshots);
  }, [snapshots]);

  console.log(snapshotTree)

  return (
    <Box sx={{ width: '100%', padding: 2}}>
        <Typography className="glass-text" variant="subtitle2" align="right" >
        Snapshots 
      </Typography>
      <Typography className="glass-text" variant="subtitle2" align="right"
                                sx={{fontSize: 24, marginBottom: 4}}>
        {database} / {table}
      </Typography>
      <Tabs value={tabValue} onChange={handleTabChange} aria-label="snapshot tabs">
        <Tab label="Snapshots" />
        <Tab label="Tags" />
        <Tab label="Branches" />
      </Tabs>
      {tabValue === 0 && (
        <TreeView
          defaultCollapseIcon={<ExpandMoreIcon />}
          defaultExpandIcon={<ChevronRightIcon />}
          sx={{ height: 240, flexGrow: 1, maxWidth: 800, overflowY: 'auto', marginLeft: '2rem' }}
        >
          {renderTree(snapshotTree)}
        </TreeView>
      )}
      {tabValue === 1 && (
        <Box sx={{ p: 3 }}>
          <List >
        {tags.map((tag) => (
          <ListItem button key={tag.name}>
            <ListItemText primary={tag.name} secondary={`Snapshot ID: ${tag.snapshot_id}`} />
          </ListItem>
        ))}
      </List>
        </Box>
      )}
      {tabValue === 2 && (
        <Box sx={{ p: 3 }}>
          <List >
        {branches.map((branch) => (
          <ListItem button key={branch.name}>
            <ListItemText primary={branch.name} secondary={`Snapshot ID: ${branch.snapshot_id}`} />
          </ListItem>
        ))}
      </List>
      </Box>
      )}
    </Box>
  );
}