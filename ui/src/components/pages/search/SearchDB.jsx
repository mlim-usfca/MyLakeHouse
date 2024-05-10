import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { SearchBar } from './SearchBar.jsx';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import { Box, Typography } from '@mui/material';
import { getDatabaseList } from '@/services/search/services.js';

export const SearchDB = () => {
  const [databaseList, setDatabaseList] = useState([]);
  const [searchResults, setSearchResults] = useState([]);

  useEffect(() => {
    // Fetch initial database list from the backend
    fetchDatabaseList();
  }, []);

  const fetchDatabaseList = async () => {
    try {
      const response =await getDatabaseList();
      setDatabaseList(response.db_list ?? []); // Update database list state
      setSearchResults(response.db_list ?? []); // Initialize search results with the fetched data
    } catch (error) {
      console.error('Error fetching database list:', error);
    }
  };

  const handleSearch = (searchTerm) => {
    const filteredResults = databaseList.filter(item =>
      item.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setSearchResults(filteredResults);
  };

  return (
    <Box sx={{ width: '100%', padding:2 }}>
        <Typography className="glass-text" variant="subtitle2" align="right" sx={{paddingRight: 2, fontSize: 40}}>
            Search For Database
        </Typography>
      <SearchBar onSearch={handleSearch} />
      <Box sx={{ width: '100%', paddingLeft: 2 }}>
        <List>
          {searchResults.map((result, index) => (
            <ListItem key={"db-"+index}>
              <Link to={`/searchtable/${result}`}>{result}</Link>
            </ListItem>
          ))}
        </List>
      </Box>
    </Box>
  );
};



