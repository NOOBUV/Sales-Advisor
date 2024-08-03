import React from 'react';
import { ListItem, ListItemText, Typography, Box } from '@mui/material';

function Chat({ chat }) {
  return (
    <ListItem alignItems="flex-start">
      <Box sx={{ width: '100%' }}>
        <ListItemText
          primary={chat.user}
          secondary={
            <React.Fragment>
              <Typography
                sx={{ display: 'inline' }}
                component="span"
                variant="body2"
                color="text.primary"
              >
                {chat.message}
              </Typography>
            </React.Fragment>
          }
        />
      </Box>
    </ListItem>
  );
}

export default Chat;