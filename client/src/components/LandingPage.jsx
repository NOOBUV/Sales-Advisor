import React from 'react';
import { Link } from 'react-router-dom';
import { Container, Typography, Button, Box } from '@mui/material';

function LandingPage() {
  return (
    <Container maxWidth="md" sx={{ height: '100vh', display: 'flex', alignItems: 'center' }}>
      <Box sx={{ width: '100%', textAlign: 'center' }}>
        <Typography variant="h2" component="h1" gutterBottom>
          Welcome to Sales Advisor
        </Typography>
        <Typography variant="h5" component="h2" gutterBottom>
          Your AI-powered sales assistant
        </Typography>
        <Box sx={{ mt: 4 }}>
          <Button component={Link} to="/login" variant="contained" color="primary" sx={{ mr: 2 }}>
            Login
          </Button>
          <Button component={Link} to="/signup" variant="outlined" color="primary">
            Sign Up
          </Button>
        </Box>
      </Box>
    </Container>
  );
}

export default LandingPage;