import axios from "axios";
import { DEV } from "../service";


export const getDatabaseList = async () => {
    try {
      const response = await axios.get(DEV + 'dashboard/list-databases');
      return response.data;
    } catch (error) {
      // Handle error
      console.error("Error fetching database list:", error);
      throw error; // Optionally rethrow the error
    }
  };
  
export const getTableList = async (dbName) => {
try {
    const response = await axios.get(DEV + `dashboard/list-tables/?db_name=${dbName}`);
    return response.data;
} catch (error) {
    // Handle error
    console.error(`Error fetching table list for database ${dbName}:`, error);
    throw error; // Optionally rethrow the error
}
};