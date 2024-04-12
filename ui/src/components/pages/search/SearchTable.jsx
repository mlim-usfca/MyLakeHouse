import React, { useState, useEffect } from 'react';
import {Link, useNavigate, useParams} from 'react-router-dom';
import { SearchBar } from './SearchBar.jsx';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import { Box, Typography } from '@mui/material';
import axios from 'axios';
import ListItemButton from "@mui/material/ListItemButton";
import {useRecentViewDispatch} from "@/contexts/recent-view-history.jsx";
import IconButton from "@mui/material/IconButton";
import NavigateNextIcon from '@mui/icons-material/NavigateNext';

export const SearchTable = () => {
  const { database } = useParams();
  const [tableList, setTableList] = useState([]);
  const [searchResults, setSearchResults] = useState([]);
  const navigate = useNavigate();
  const recentViewDispatch = useRecentViewDispatch()
  useEffect(() => {
    fetchTableList(database);
  }, [database]);

  const fetchTableList = async (dbName) => {
    try {
      const response = await axios.get(`http://localhost:8090/dashboard/list-tables/?db_name=${dbName}`);
      console.log(response.data);
      setTableList(response.data); // Update table list state
      setSearchResults(response.data); // Initialize search results with the fetched data
    } catch (error) {
      console.error('Error fetching table list:', error);
    }
  };

  const handleSearch = (searchTerm) => {
    console.log('Searching for:', searchTerm);
    const filteredResults = tableList.filter(item =>
      item.table_name.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setSearchResults(filteredResults);
  };

  return (
    <Box sx={{ width: '100%', typography: 'body1', padding: 2 }}>
        <Typography className="glass-text" variant="subtitle2" align="right" >
            {database}/Search For Table
        </Typography>
      <SearchBar onSearch={handleSearch} />
      <List>
        {searchResults.map((result, index) => (
          <ListItem key={index}
                    secondaryAction={
                      <ListItemButton
                          onClick={() => {
                            recentViewDispatch({ type: "add", value: { db: database, table: result.table_name } })
                            navigate(`/table/${database}/${result.table_name}`)
                          }}
                      >
                        <ListItemText primary="Enter Table"/>
                        <NavigateNextIcon />
                      </ListItemButton>
                    }
          >
            <ListItemText primary={result.table_name} />
          </ListItem>
        ))}
      </List>
    </Box>
  );
};




