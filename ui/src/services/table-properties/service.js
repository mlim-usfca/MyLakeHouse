import axios from "axios";


export const updateProp = async ({db, tbl, props}) => {
    return await axios.post(`${import.meta.env.VITE_HOST}/props/alterTableProps`, {
        table_name: tbl,
        db_name: db,
        properties : props
    })
}