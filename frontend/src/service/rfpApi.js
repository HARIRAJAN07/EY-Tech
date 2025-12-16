import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

export const checkRfps = async () => {
  const response = await axios.post(`${API_BASE}/rfp/check`);
  return response.data;
};

export const analyzeTechnically = async (fileName) => {
  const response = await axios.post(
    `${API_BASE}/tech/analyze`,
    { file_name: fileName }
  );
  return response.data;
};
