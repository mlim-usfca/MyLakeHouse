import { useState } from 'react'
import { Outlet } from 'react-router-dom';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Unstable_Grid2';
import Paper from '@mui/material/Paper';
import { styled } from '@mui/material/styles';


const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: 'center',
  color: theme.palette.text.secondary,
}));


function App() {

  return (
    <>
    <CssBaseline/>
    <Container maxWidth={false} disableGutters style={{ height: '100vh' }}>
      <Box sx={{ bgcolor: '#cfe8fc', height: "100%", padding: "20px 12px" }}>
        <Grid container columnSpacing={1} style={{ height: "100%", width: "100%" }}>
          <Grid item xs={3}>
            <Box height="100%">
              <Paper style={{ height: '100%'}}>
                {/* Your content here */}
                Left Column
              </Paper>
            </Box>
          </Grid>
          <Grid item xs={9}>
            <Box height="100%">
              <Paper style={{ height: '100%'}}>
                {/* Your content here */}
                <Outlet/>
              </Paper>
            </Box>
          </Grid>
        </Grid>
      </Box>
    </Container>
    </>
  );
}

export default App
