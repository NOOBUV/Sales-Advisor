import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { v4 as uuidv4 } from 'uuid'; // Import uuid
import { Container, Box, TextField, Button, List, ListItem, ListItemText, ListItemAvatar, Avatar, Typography, CircularProgress } from '@mui/material';
import ReactMarkdown from 'react-markdown';
import { useAuth } from '../AuthContext';

const SalesAdvisor = () => {
  const [chats, setChats] = useState([]);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const { logout } = useAuth();
  const bottomRef = useRef(null);

  useEffect(() => {
    const fetchChats = async () => {
      try {
        const response = await axios.get('https://utkarsh-fse-mha4s7stfa-uc.a.run.app0/api/chats', {
          headers: { Authorization: `Token ${localStorage.getItem('token')}` },
        });
        setChats(response.data.map(chat => ({ ...chat, id: uuidv4() }))); // Assign unique ID
      } catch (error) {
        if (error.response && error.response.status === 401) {
          logout();
        } else {
          console.error('Failed to fetch chats', error);
        }
      }
    };

    fetchChats();
  }, [logout]);

  useEffect(() => {
    // Scroll to the bottom whenever chats update
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chats]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!message.trim()) return;

    setLoading(true);
    try {
      const response = await axios.post(
        'https://utkarsh-fse-mha4s7stfa-uc.a.run.app0/api/query/',
        { question: message },
        {
          headers: { Authorization: `Token ${localStorage.getItem('token')}` },
        }
      );

      setChats(prevChats => [...prevChats, { ...response.data, id: uuidv4() }]); // Add unique ID
      setMessage('');
    } catch (error) {
      console.error('Failed to send message', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container>
      <Box sx={{ height: '80vh', overflowY: 'auto', mb: 2, mt: 2 }}>
        <List>
          {chats.map((chat) => (
            <React.Fragment key={chat.id}> {/* Use unique ID */}
              <ListItem>
                <ListItemAvatar>
                  <Avatar>{/* User icon */}</Avatar>
                </ListItemAvatar>
                <ListItemText primary={<Typography sx={{ color: '#2196f3' }}>{chat.question}</Typography>} />
              </ListItem>
              <ListItem>
                <ListItemText 
                  primary={
                    <Typography component="div">
                      <ReactMarkdown>{chat.summary}</ReactMarkdown>
                    </Typography>
                  } 
                />
              </ListItem>
            </React.Fragment>
          ))}
          <div ref={bottomRef} />
        </List>
      </Box>
      <Box component="form" onSubmit={handleSendMessage} sx={{ display: 'flex', alignItems: 'center' }}>
        <TextField
          variant="outlined"
          fullWidth
          placeholder="Type your message"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          sx={{ mr: 2 }}
        />
        {loading ? (
          <CircularProgress />
        ) : (
          <Button type="submit" variant="contained">
            Send
          </Button>
        )}
      </Box>
    </Container>
  );
};

export default SalesAdvisor;
