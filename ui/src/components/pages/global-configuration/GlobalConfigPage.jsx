import React from 'react'
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Stack from '@mui/material/Stack';



export const GlobalConfigPage = () => {
    const [settings, setSettings] = React.useState({snapShotFreq: '', compaction: ''});
    const handleChange = (event) => {
        setSettings(() => ({...settings, [event.target.name]: event.target.value }));
    };
    return <Box sx={{ width: '100%'}}>
        <Typography className="glass-text" variant="subtitle2" align="right" sx={{paddingRight: 2, fontSize: 40}}>
            Settings
        </Typography>

        <Box sx={{ width: '50%', padding: 2}}>
            <Box sx={{marginBottom: 4}}>
                <Typography variant="h5" gutterBottom>
                    Snapshot Retention Policy
                </Typography>
                <Divider sx={{marginBottom: 1}}/>
                <Typography variant="body1" gutterBottom>
                    body1. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quos
                    blanditiis tenetur unde suscipit, quam beatae rerum inventore consectetur,
                    neque doloribus, cupiditate numquam dignissimos laborum fugiat deleniti? Eum
                    quasi quidem quibusdam.
                </Typography>

                <FormControl sx={{ m: 1, minWidth: 120}}>
                    <Stack spacing={2}>
                        <Box sx={{width: "100%", display: 'flex', flexDirection: "column"}}>
                            <Typography variant="p" gutterBottom>
                                Time Frequency
                            </Typography>
                            <Select
                                labelId="demo-simple-select-helper-label"
                                id="demo-simple-select-helper"
                                value={settings.snapShotFreq}
                                onChange={handleChange}
                                name="snapShotFreq"
                            >
                                <MenuItem value="">
                                    <em>None</em>
                                </MenuItem>
                                <MenuItem value={10}>Ten</MenuItem>
                                <MenuItem value={20}>Twenty</MenuItem>
                                <MenuItem value={30}>Thirty</MenuItem>
                            </Select>
                        </Box>
                    </Stack>
                </FormControl>
            </Box>
            <Box sx={{marginBottom: 4}}>
                <Typography variant="h5" gutterBottom>
                    Compaction Policy
                </Typography>
                <Divider sx={{marginBottom: 1}}/>
                <Typography variant="body1" gutterBottom>
                    body1. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quos
                    blanditiis tenetur unde suscipit, quam beatae rerum inventore consectetur,
                    neque doloribus, cupiditate numquam dignissimos laborum fugiat deleniti? Eum
                    quasi quidem quibusdam.
                </Typography>
                <FormControl sx={{ m: 1, minWidth: 120 }}>
                    <Stack spacing={2}>
                        <Box sx={{width: "100%", display: 'flex', flexDirection: "column"}}>
                            <Typography variant="p" gutterBottom>
                                Policy
                            </Typography>
                            <Select
                                labelId="demo-simple-select-helper-label"
                                id="demo-simple-select-helper"
                                value={settings.compaction}
                                name="compaction"
                                onChange={handleChange}
                            >
                                <MenuItem value="">
                                    <em>None</em>
                                </MenuItem>
                                <MenuItem value={10}>Ten</MenuItem>
                                <MenuItem value={20}>Twenty</MenuItem>
                                <MenuItem value={30}>Thirty</MenuItem>
                            </Select>
                        </Box>
                    </Stack>
                </FormControl>
            </Box>
        </Box>
    </Box>
}