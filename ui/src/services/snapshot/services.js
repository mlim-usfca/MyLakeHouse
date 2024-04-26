import axios from "axios";
import { DEV } from "../service";


export const getSnapshotList = async (database, table) => {
    try {
        const response = await axios.get(DEV + `dashboard/snapshots?branch_name=main&db_name=${database}&table_name=${table}`);
      return response.data;
    } catch (error) {
      // Handle error
      console.error("Error fetching database list:", error);
      throw error; // Optionally rethrow the error
    }
  };
  

  export const getSnapshoData = async (database, table, id) => {
    try {
        const response = await axios.get(DEV + `dashboard/snapshot?db_name=${database}&table_name=${table}&snapshot_id=${id}`);
        console.log(response.data);
      return response.data;
    } catch (error) {
      // Handle error
      console.error("Error fetching database list:", error);
      throw error; // Optionally rethrow the error
    }
  };