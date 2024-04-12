import React, {useEffect} from 'react'
import {Outlet} from 'react-router-dom';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Unstable_Grid2';
import Paper from '@mui/material/Paper';
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Divider from '@mui/material/Divider';
import PublicIcon from '@mui/icons-material/Public';
import SearchIcon from '@mui/icons-material/Search';
import DeleteIcon from '@mui/icons-material/Delete';

// import { styled } from '@mui/material/styles';
import axios from "axios"
import Typography from '@mui/material/Typography';
import { useNavigate } from "react-router-dom";
import {useRecentView, useRecentViewDispatch} from "@/contexts/recent-view-history.jsx";
import IconButton from "@mui/material/IconButton";


// const Item = styled(Paper)(({ theme }) => ({
//   backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
//   ...theme.typography.body2,
//   padding: theme.spacing(1),
//   textAlign: 'center',
//   color: theme.palette.text.secondary,
// }));


export const App = () => {

    const [selectedIndex, setSelectedIndex] = React.useState(1);
    const navigate = useNavigate();
    const recentView = useRecentView();
    const recentViewDispatch = useRecentViewDispatch();

    console.log(recentView, "recent view")

    const handleListItemClick = (
        event,
        index,
    ) => {
        if (index === 1 && selectedIndex !== 1) {
            navigate("/config")
        } else if (index === 0 && selectedIndex !== 0) {
            navigate("/")
        }
        setSelectedIndex(index);
    };

    useEffect(() => {
        axios.get("http://localhost:8090/test").then(data => console.log(data))
    }, []);


    return (
        <>
            <CssBaseline/>
            <div className="shape"></div>
            <Container maxWidth={false} disableGutters style={{height: '100vh',position: 'relative',
                zIndex: 1}}>
                <Box sx={{
                    background: 'radial-gradient(ellipse at top, #1E7D5B, transparent),\n' +
                        '            radial-gradient(ellipse at bottom, #155D78, transparent)',
                    height: "100%", padding: "20px 12px"
                }}>
                    <Grid container columnSpacing={4} style={{height: "100%", width: "100%"}}>
                        <Grid item xs={3}>
                            <Box height="100%">
                                <Paper style={{
                                    background: 'rgba(255, 255, 255, 0.2)', borderRadius: '10px',
                                    boxShadow: '0 8px 32px 0 rgba( 31, 38, 135, 0.37 )',
                                    marginLeft: "1rem",
                                    height: '100%',
                                    backdropFilter:"blur(8px)",

                                }}>
                                    <Typography className="glass-text" variant="subtitle2" align="right"
                                                sx={{padding: "8px 16px 0 0", fontSize: 16}}>
                                        Caspian
                                    </Typography>
                                    <Box sx={{width: '100%', bgcolor: 'transparent'}}>
                                        <List component="nav" aria-label="main mailbox folders">
                                            <ListItemButton
                                                selected={selectedIndex === 0}
                                                onClick={(event) => handleListItemClick(event, 0)}
                                            >
                                                <ListItemIcon>
                                                    <SearchIcon/>
                                                </ListItemIcon>
                                                <ListItemText primary="Search"/>
                                            </ListItemButton>
                                            <ListItemButton
                                                selected={selectedIndex === 1}
                                                onClick={(event) => handleListItemClick(event, 1)}
                                            >
                                                <ListItemIcon>
                                                    <PublicIcon/>
                                                </ListItemIcon>
                                                <ListItemText primary="Globlal Settings"/>
                                            </ListItemButton>
                                            <ListItemButton
                                                selected={selectedIndex === 2}
                                                onClick={(event) => handleListItemClick(event, 2)}
                                            >
                                                <ListItemText primary="Recent Activity"/>
                                            </ListItemButton>
                                            <Divider/>
                                            {recentView?.tables?.map(rc => {
                                                return  <ListItemButton key={"rc-view-" + rc.table}
                                                    onClick={(event) => navigate(`/table/${rc.db}/${rc.table}`)}
                                                >
                                                    <ListItemText primary={`${rc.db}.${rc.table}`}/>
                                                    <IconButton onClick={() => recentViewDispatch({type: "remove", value: {db: rc.db, table: rc.table}})}>
                                                        <DeleteIcon />
                                                    </IconButton>
                                                </ListItemButton>
                                            })}

                                        </List>
                                    </Box>
                                </Paper>
                            </Box>
                        </Grid>
                        <Grid item xs={9}>
                            <Box height="100%">
                                <Paper className="paper" style={{
                                    background: 'rgba(255, 255, 255, 0.2)', borderRadius: '10px',
                                    boxShadow: '0 8px 32px 0 rgba( 31, 38, 135, 0.37 )',
                                    height: '100%',
                                    backdropFilter:"blur(8px)",
                                }}>
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
