import React, { useState } from 'react';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

export const SearchBar = ({ onSearch }) => {
  const [searchTerm, setSearchTerm] = useState('');

  const handleChange = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onSearch(searchTerm);
  };

  return (
    <form
      onSubmit={handleSubmit}
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        margin: '20px 0',
      }}
    >
      <TextField
        type="text"
        placeholder="Search..."
        value={searchTerm}
        onChange={handleChange}
        variant="outlined"
        size="small"
        fullWidth
        style={{ margin: '1rem' }}
      />
      <Button type="submit" variant="contained" color="primary" style={{ marginRight: '1rem' }}>
        Search
      </Button>
    </form>
  );
};
