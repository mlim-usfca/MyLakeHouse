import axios from "axios";


export const updateProp = async ({db, tbl, props}) => {
    return await axios.post(`http://localhost:8090/props/alterTableProps`, {
        table_name: tbl,
        db_name: db,
        properties : props
    })
}