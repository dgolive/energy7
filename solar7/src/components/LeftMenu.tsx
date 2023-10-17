// LeftMenu.tsx
import React, { useState } from 'react';
import { TextField, Button } from '@mui/material';
import { Link } from 'react-router-dom';


const LeftMenu = () => {
  const [address, setAddress] = useState('');

  const handleSearch = () => {
    // Use the address to fetch coordinates and data from Google Maps API.
  };

  return (
    <div>
      <TextField
        label="Address"
        variant="outlined"
        value={address}
        onChange={(e) => setAddress(e.target.value)}
      />
      <Button variant="contained" color="primary" onClick={handleSearch}>
        Search
      </Button>
    </div>
  );
};

export default LeftMenu;
