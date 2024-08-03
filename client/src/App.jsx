import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import theme from './theme';
import Navbar from './components/Navbar';
import LandingPage from './components/LandingPage';
import Login from './components/Login';
import Signup from './components/Signup';
import SalesAdvisor from './components/SalesAdvisor';
import EditDatabase from './components/EditDatabase';
import { AuthProvider, useAuth } from './AuthContext';
import './App.css';

const ProtectedRoute = ({ children }) => {
  const { isLoggedIn } = useAuth();
  return isLoggedIn ? children : <Navigate to="/login" />;
};

const RedirectIfLoggedInRoute = ({ children }) => {
  const { isLoggedIn } = useAuth();
  return !isLoggedIn ? children : <Navigate to="/sales-advisor" />;
};

function App() {
  return (
    <AuthProvider>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router>
          <Navbar />
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<RedirectIfLoggedInRoute><Login /></RedirectIfLoggedInRoute>} />
            <Route path="/signup" element={<RedirectIfLoggedInRoute><Signup /></RedirectIfLoggedInRoute>} />
            <Route path="/sales-advisor" element={<ProtectedRoute><SalesAdvisor /></ProtectedRoute>} />
            <Route 
              path="/edit-database" 
              element={
                <ProtectedRoute>
                  <EditDatabase />
                </ProtectedRoute>
              } 
            />
          </Routes>
        </Router>
      </ThemeProvider>
    </AuthProvider>
  );
}

export default App;
