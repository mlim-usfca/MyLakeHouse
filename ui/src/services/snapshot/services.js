import axios from "axios";
import { DEV } from "../service";


export const getSnapshotList = async (database, table) => {
    try {
        const response = await axios.get(DEV + `dashboard/snapshots?branch_name=main&db_name=${database}&table_name=${table}`);
      return response.data;
    } catch (error) {
      // Handle error
      console.error("Error fetching snapshot list:", error);
      throw error; // Optionally rethrow the error
    }
  };
  

  export const getSnapshoData = async (database, table, id) => {
    try {
        const response = await axios.get(DEV + `dashboard/snapshot?db_name=${database}&table_name=${table}&snapshot_id=${id}`);
      return response.data;
    } catch (error) {
      // Handle error
      console.error("Error fetching snapshot detail:", error);
      throw error; // Optionally rethrow the error
    }
  };

  export const deleteSnapshot = async (database, table, id) => {
    try {
        const response = await axios.get(DEV + `dashboard/expire-snapshot?db_name=${database}&table_name=${table}&snapshot_id=${id}`);
      return response;
    } catch (error) {
      // Handle error
      console.error("Error expire snapshot:", error);
      throw error; // Optionally rethrow the error
    }
  };