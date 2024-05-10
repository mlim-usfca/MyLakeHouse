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
                <Typography className="glass-text" sx={{fontSize: 24, textAlign: "left"}} gutterBottom>
                    Snapshot Retention Policy
                </Typography>
                <Divider sx={{marginBottom: 1}}/>
                <Typography className="glass-text-12" textAlign="left" sx={{textTransform: 'none'}} gutterBottom>
                    Regularly expiring snapshots is recommended to delete data files that are no longer needed, and to keep the size of table metadata small.
                </Typography>

                <FormControl sx={{ m: 1, minWidth: 120}}>
                    <Stack spacing={2}>
                        <Box sx={{width: "100%", display: 'flex', flexDirection: "column"}}>
                            <Typography className="glass-text-12" sx={{textAlign: 'left'}} variant="p" gutterBottom>
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
                <Typography className="glass-text" sx={{fontSize: 24, textAlign: "left"}} gutterBottom>
                    Compaction Policy
                </Typography>
                <Divider sx={{marginBottom: 1}}/>
                <Typography className="glass-text-12" textAlign="left" sx={{textTransform: 'none'}} gutterBottom>
                    Iceberg tracks each data file in a table. More data files leads to more metadata stored in manifest files, and small data files causes an unnecessary amount of metadata and less efficient queries from file open costs.
                    Iceberg can compact data files in parallel using Spark with the rewriteDataFiles action. This will combine small files into larger files to reduce metadata overhead and runtime file open cost.                </Typography>
                <FormControl sx={{ m: 1, minWidth: 120 }}>
                    <Stack spacing={2}>
                        <Box sx={{width: "100%", display: 'flex', flexDirection: "column"}}>
                            <Typography className="glass-text-12" textAlign="left" variant="p" gutterBottom>
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