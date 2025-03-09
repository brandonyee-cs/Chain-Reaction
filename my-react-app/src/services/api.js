// src/services/api.js
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

/**
 * Generate supply chain analysis for a business
 * @param {string} businessId - The business ID
 * @returns {Promise<Object>} - Supply chain data
 */
export const generateSupplyChain = async (businessId) => {
  console.log(`🚀 Calling generateSupplyChain API for business ID: ${businessId}`);
  console.log(`🔗 API URL: ${API_BASE_URL}/generate-supply-chain/`);
  
  try {
    const requestData = { business_id: businessId };
    console.log(`📤 Request payload:`, requestData);
    
    const response = await fetch(`${API_BASE_URL}/generate-supply-chain/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify(requestData),
    });
    
    console.log(`📥 Response status:`, response.status);
    
    // Handle non-OK responses
    if (!response.ok) {
      const errorText = await response.text();
      console.error(`❌ API error (${response.status}):`, errorText);
      throw new Error(`API error: ${response.status} ${response.statusText}. Details: ${errorText}`);
    }

    const data = await response.json();
    console.log(`✅ Response data:`, data);
    return data;
  } catch (error) {
    console.error(`❌ Exception in generateSupplyChain:`, error);
    throw error;
  }
};

/**
 * Generate investment portfolio based on supply chain
 * @param {Object} params - Investment parameters
 * @returns {Promise<Object>} - Investment portfolio data
 */
export const generateInvestment = async (params) => {
  console.log(`🚀 Calling generateInvestment API with params:`, params);
  console.log(`🔗 API URL: ${API_BASE_URL}/generate-investment/`);
  
  try {
    const response = await fetch(`${API_BASE_URL}/generate-investment/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify(params),
    });
    
    console.log(`📥 Response status:`, response.status);
    
    // Handle non-OK responses
    if (!response.ok) {
      const errorText = await response.text();
      console.error(`❌ API error (${response.status}):`, errorText);
      throw new Error(`API error: ${response.status} ${response.statusText}. Details: ${errorText}`);
    }

    const data = await response.json();
    console.log(`✅ Response data:`, data);
    return data;
  } catch (error) {
    console.error(`❌ Exception in generateInvestment:`, error);
    throw error;
  }
};

// Add a simple health check function to test API connectivity
export const checkApiHealth = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/docs`, {
      method: 'GET',
      headers: {
        'Accept': 'text/html',
      },
    });
    
    return {
      status: response.status,
      ok: response.ok,
      statusText: response.statusText,
    };
  } catch (error) {
    console.error('API health check failed:', error);
    return {
      status: 0,
      ok: false,
      statusText: error.message,
      error
    };
  }
};