import React, { useState } from 'react';
import { Link, useParams  } from 'react-router-dom'; // Import Link from react-router-dom
import {SearchBar} from './SearchBar.jsx';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import { Box, Typography } from '@mui/material';
import {tables} from '../../../../public/testdata.js'

export const SearchTable = () => {
  let { database } = useParams();
  // We will call our backend api and give them the db name as parameter to get the table name list later
  const initialList = tables[database];
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
        {database}/Search for Table
      </Typography>
      <SearchBar onSearch={handleSearch} />
      <List>
        {searchResults.map((result, index) => (
          <ListItem key={index}>
            <ListItemText primary={result} />
            <Link to={`/table/${database}/${result}`}>Enter Table</Link>
          </ListItem>
        ))}
      </List>
    </Box>
  );
};


