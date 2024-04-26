import axios from 'axios';
import { DEV } from '../service';

export async function fetchData(database, table) {

  try {
    const getTableInfoResponse = await axios.get(`${DEV}metadata/getTableInfo?db_name=${database}&table_name=${table}`);
    const getSchemaResponse = await axios.get(`${DEV}metadata/getSchema?db_name=${database}&table_name=${table}`);

    // Process the responses
    const tableInfoData = getTableInfoResponse.data;
    const schemaData = getSchemaResponse.data;

    // Return the data or do something else with it
    return { tableInfoData, schemaData };
  } catch (error) {
    // Handle errors
    console.error('Error fetching data:', error);
    throw error; // You might want to handle errors differently, like displaying an error message to the user
  }
}