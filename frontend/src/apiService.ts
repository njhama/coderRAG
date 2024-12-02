import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

export const fetchRAGResults = async (query: string, k: number = 3) => {
  const response = await axios.post(`${API_BASE_URL}/retrieve`, { query, k });
  return response.data;
};
