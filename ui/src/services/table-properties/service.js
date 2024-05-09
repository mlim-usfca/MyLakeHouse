import axios from "axios";


export const updateProp = async ({db, tbl, props}) => {
    return await axios.post(`${import.meta.env.VITE_HOST}:${import.meta.env.VITE_BE_API_PORT}/props/alterTableProps`, {
        table_name: tbl,
        db_name: db,
        properties : props
    })
}