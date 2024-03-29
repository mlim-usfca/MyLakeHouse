import React, { useState } from 'react';
import { Link } from 'react-router-dom'; // Import Link from react-router-dom
import {SearchBar} from './SearchBar.jsx';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import { Box, Typography } from '@mui/material';
import {databaseList} from '../../../../public/testdata.js'

export const SearchDB = () => {
  // We will call our backend api to get the database name list later
  const initialList = databaseList;
  const [searchResults, setSearchResults] = useState(initialList);

  const handleSearch = (searchTerm) => {
    // Perform search logic here
    console.log('Searching for:', searchTerm);
    // Update search results
    const filteredResults = initialList.filter(item =>
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


