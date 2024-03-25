import React, { useState } from 'react';
import { TreeView } from '@mui/x-tree-view/TreeView';
import { TreeItem } from '@mui/x-tree-view/TreeItem';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import { Tabs, Tab, Box, Typography } from '@mui/material';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import { useParams } from 'react-router-dom';
import {snapshots, tags, branches} from '../../../../public/testdata.js'

// Recursive function to render TreeItems
const renderTree = (node) => (
  <TreeItem key={node.snapshotId} nodeId={node.snapshot_id} label={`Snapshot ${node.snapshot_id} Time ${node.committed_at}`}>
    {Array.isArray(node.children) ? node.children.map((childNode) => renderTree(childNode)) : null}
  </TreeItem>
);

export const SnapshotPage = () => {
  let { database, table } = useParams();
  
  // Provide default values for testing now 
  database = database || 'Test Database';
  table = table || 'Test Table';

  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  return (
    <Box sx={{ width: '100%', typography: 'body1' }}>
      <Typography variant="p" component="p" sx={{ textAlign: 'left' }}>
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
          {renderTree(snapshots)}
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