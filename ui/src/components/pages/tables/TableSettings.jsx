import React, {useEffect, useState} from 'react'
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import {properties} from "@/assets/default-properties.js";
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import IconButton from '@mui/material/IconButton';
import SearchIcon from '@mui/icons-material/Search';
import {useParams} from "react-router-dom";
import axios from "axios";
import {updateProp} from "@/services/table-properties/service.js"
import Grid from "@mui/material/Unstable_Grid2";



export const TableSettings = () => {

    const { db, tbl } = useParams();
    const [data, setData] = useState(properties)
    const [filteredData, setFilteredData] = useState(data)
    useEffect(() => {
        axios.get(`http://localhost:8090/props/getTableProps?db_name=${db}&table_name=${tbl}`)
            .then(data => {
                setData( prevState => {
                    Object.entries(data?.data).forEach(([name, value]) => {
                        const prop = prevState.find(p => p.property === name)
                        if (prop) {
                            prop.value = value;
                        }
                    })
                    return [...prevState]
                })
                setFilteredData( prevState => {
                    Object.entries(data?.data).forEach(([name, value]) => {
                        const prop = prevState.find(p => p.property === name)
                        if (prop) {
                            prop.value = value;
                        }
                    })
                    return [...prevState]
                })
            })
    }, [db, tbl]);
    const handleSearch = ({target: {value}}) => {
        setFilteredData(data.filter(p => p.property.includes(value)))
    };

    const onChange = async (e) => {
        const {name, value} = e.target
        const res = await updateProp({db, tbl, props: [{[name]: value}]});

        console.log(res)

        setData(prevState => {
            const prop = prevState.find(p => p.property === name)
            if (prop) {
                prop.value = value;
            }
            return [...prevState]
        })

        setFilteredData(prevState => {
            const prop = prevState.find(p => p.property === name)
            if (prop) {
                prop.value = value;
            }
            return [...prevState]
        })
    }

    return <Box sx={{width: '100%', padding: 2}}>
        <Typography className="glass-text" variant="subtitle2" align="right" >
            Table Properties
        </Typography>

        <Box sx={{ flexGrow: 1 }}>
            <Grid container spacing={2}>
                <Grid xs={8}>
                    <TextField
                        sx={{marginBottom: 2}}
                        variant="outlined"
                        placeholder="Search..."
                        onChange={handleSearch}
                        InputProps={{
                            endAdornment: (
                                <IconButton aria-label="search">
                                    <SearchIcon />
                                </IconButton>
                            ),
                        }}
                    />
                </Grid>
                <Grid xs={4}>
                    <Typography className="glass-text" variant="subtitle2" align="right"
                                sx={{fontSize: 24, marginBottom: 4}}>
                        {`${db}.${tbl}`}
                    </Typography>
                </Grid>
            </Grid>
        </Box>
        <TableContainer component={Paper} sx={{backgroundColor: 'transparent', width: '100%',
            padding: '16px',
            maxHeight: '800px',
            scrollBehavior: 'smooth'}}>
        <Table sx={{minWidth: 650}} aria-label="simple table">
            <TableHead>
                <TableRow>
                    <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}}>Property</TableCell>
                    <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}} align="left">Config</TableCell>
                </TableRow>
            </TableHead>
            <TableBody>
                {filteredData.map((row) => (
                    <TableRow
                        key={row.property}
                        sx={{'&:last-child td, &:last-child th': {border: 0}}}
                    >
                        <TableCell sx={{borderBottom: "1px solid rgba(0, 0, 0, .1)"}} component="th" scope="row">
                            {row.property}
                        </TableCell>
                        <TableCell align="left" sx={{ minWidth: 120, borderBottom: "1px solid rgba(0, 0, 0, .1)" }}>
                            <Box>
                                <FormControl fullWidth>
                                    <Select
                                        labelId="demo-simple-select-label"
                                        id="demo-simple-select"
                                        name={row.property}
                                        value={row.value ? row.value.toString() : "null"}
                                        onChange={onChange}
                                    >
                                        {row.options.map((op) => {
                                           return <MenuItem key={row.property + "-" + op} value={op}>{op}</MenuItem>
                                        })}
                                    </Select>
                                </FormControl>
                            </Box>
                        </TableCell>
                    </TableRow>
                ))}
            </TableBody>
        </Table>
    </TableContainer>
    </Box>
}