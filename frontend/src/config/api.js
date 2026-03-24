import axios from "axios";

// Update this URL mapping if your local network IP changes.
export const API_BASE_URL = "http://localhost:8000";

// Create and export a pre-configured axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
