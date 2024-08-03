import React, { useState, useEffect } from 'react';
import { Container, Typography, TextField, Button, Box } from '@mui/material';
import axios from 'axios';

const EditDatabase = () => {
  const [databaseDetails, setDatabaseDetails] = useState({
    name: '',
    connection_string: '',
    // Add other fields as necessary
  });

  useEffect(() => {
    // Fetch current database details
    const fetchDatabaseDetails = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/database/', {
          headers: { Authorization: `Token ${localStorage.getItem('token')}` },
        });
        setDatabaseDetails(response.data);
      } catch (error) {
        console.error('Failed to fetch database details', error);
      }
    };

    fetchDatabaseDetails();
  }, []);

  const handleChange = (e) => {
    setDatabaseDetails({
      ...databaseDetails,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.put('http://localhost:8000/api/database/', databaseDetails, {
        headers: { Authorization: `Token ${localStorage.getItem('token')}` },
      });
      alert('Database details updated successfully');
    } catch (error) {
      console.error('Failed to update database details', error);
      alert('Failed to update database details');
    }
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Edit Database Details
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            margin="normal"
            name="name"
            label="Database Name"
            value={databaseDetails.name}
            onChange={handleChange}
          />
          <TextField
            fullWidth
            margin="normal"
            name="connection_string"
            label="Connection String"
            value={databaseDetails.connection_string}
            onChange={handleChange}
          />
          {/* Add other fields as necessary */}
          <Button
            type="submit"
            variant="contained"
            color="primary"
            sx={{ mt: 2 }}
          >
            Update Database Details
          </Button>
        </form>
      </Box>
    </Container>
  );
};

export default EditDatabase;    