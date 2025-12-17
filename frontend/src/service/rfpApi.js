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

export const calculatePricing = async (finalRecommendation) => {
  const response = await axios.post(
    `${API_BASE}/pricing/calculate`,
    {
      final_recommendation: finalRecommendation,
      quantity: 10
    }
  );
  return response.data;
};

export const downloadFinalBid = async (finalBidPayload) => {
  const response = await axios.post(
    `${API_BASE}/bid/download`,
    finalBidPayload,
    {
      responseType: "blob"   // 🔑 VERY IMPORTANT FOR PDF
    }
  );
  return response;
};
