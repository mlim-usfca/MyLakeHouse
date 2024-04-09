import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { SearchBar } from './SearchBar.jsx';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import { Box, Typography } from '@mui/material';
import axios from 'axios'; 

export const SearchDB = () => {
  const [databaseList, setDatabaseList] = useState([]);
  const [searchResults, setSearchResults] = useState([]);

  useEffect(() => {
    // Fetch initial database list from the backend
    fetchDatabaseList();
  }, []);

  const fetchDatabaseList = async () => {
    try {
      const response = await axios.get('http://localhost:8090/dashboard/list-databases');
      console.log(response);
      setDatabaseList(response.data.db_list); // Update database list state
      setSearchResults(response.data.db_list); // Initialize search results with the fetched data
    } catch (error) {
      console.error('Error fetching database list:', error);
    }
  };

  const handleSearch = (searchTerm) => {
    console.log('Searching for:', searchTerm);
    const filteredResults = databaseList.filter(item =>
      item.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setSearchResults(filteredResults);
  };

  return (
    <Box sx={{ width: '100%', typography: 'body1' }}>
      <Typography variant="p" component="p" sx={{ textAlign: 'left' }}>
        Search for Database
      </Typography>
      <SearchBar onSearch={handleSearch} />
      <List>
        {searchResults.map((result, index) => (
          <ListItem key={index}>
            <ListItemText primary={result} />
            <Link to={`/searchtable/${result}`}>Enter Database</Link>
          </ListItem>
        ))}
      </List>
    </Box>
  );
};



