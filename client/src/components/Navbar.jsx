import React, { useEffect, useState } from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { useAuth } from '../AuthContext';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import axios from 'axios';

const Navbar = () => {
  const { isLoggedIn, logout } = useAuth();
  const navigate = useNavigate();
  const [isAdmin, setIsAdmin] = useState(false);

  useEffect(() => {
    const fetchUserDetails = async () => {
      if (isLoggedIn) {
        try {
          const response = await axios.get('https://utkarsh-fse-mha4s7stfa-uc.a.run.app0/api/user/', {
            headers: { Authorization: `Token ${localStorage.getItem('token')}` },
          });
          setIsAdmin(response.data.is_admin);
        } catch (error) {
          console.error('Failed to fetch user details', error);
        }
      }
    };

    fetchUserDetails();
  }, [isLoggedIn]);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography 
          variant="h6" 
          sx={{ flexGrow: 1 }}
          component={RouterLink} 
          to="/sales-advisor"
          style={{ textDecoration: 'none', color: 'inherit' }} // Styling to match MUI AppBar
        >
          Sales Advisor
        </Typography>
        {isLoggedIn && (
          <Box>
            {isAdmin && (
              <Button 
                color="inherit" 
                component={RouterLink} 
                to="/edit-database"
                sx={{ mr: 2 }}
              >
                Edit Database
              </Button>
            )}
            <Button color="inherit" onClick={handleLogout}>
              Logout
            </Button>
          </Box>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
