// src/api.js
import axios from "axios";

axios.defaults.baseURL = "http://127.0.0.1:5000";
axios.defaults.withCredentials = true;

export default axios;
