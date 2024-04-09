import React, { useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import { SearchBar } from './SearchBar.jsx';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import { Box, Typography } from '@mui/material';
import axios from 'axios'; // Import axios

export const SearchTable = () => {
  const { database } = useParams();
  const [tableList, setTableList] = useState([]);
  const [searchResults, setSearchResults] = useState([]);

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
    <Box sx={{ width: '100%', typography: 'body1' }}>
      <Typography variant="p" component="p" sx={{ textAlign: 'left' }}>
        {database} / Search for Table
      </Typography>
      <SearchBar onSearch={handleSearch} />
      <List>
        {searchResults.map((result, index) => (
          <ListItem key={index}>
            <ListItemText primary={result.table_name} />
            <Link to={`/table/${database}/${result.table_name}`}>Enter Table</Link>
          </ListItem>
        ))}
      </List>
    </Box>
  );
};




