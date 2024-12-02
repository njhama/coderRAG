import axios from "axios";

const API_BASE_URL = "http://localhost:8000"; 

export const fetchRAGResults = async (query: string) => {
  const response = await axios.post(`${API_BASE_URL}/api/query`, { query });
  return response.data; 
};
