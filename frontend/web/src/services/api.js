const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';
const DEFAULT_REGION_ID = import.meta.env.VITE_DEFAULT_REGION_ID || '1';

const buildAnalyticsQuery = (indicators, regionId) => {
  const params = new URLSearchParams();
  params.set('indicators', indicators);
  params.set('region_id', String(regionId || DEFAULT_REGION_ID));
  return params.toString();
};

export const fetchLineChart = (indicators, regionId) =>
  fetchData(`analytics/line-chart?${buildAnalyticsQuery(indicators, regionId)}`);

export const fetchPieChart = (indicators, regionId) =>
  fetchData(`analytics/pie-chart?${buildAnalyticsQuery(indicators, regionId)}`);
/**
 * Base fetch function for API requests
 * @param {string} endpoint - API endpoint to fetch from
 * @returns {Promise<any|null>} - Parsed JSON response or null on error
 */
const fetchData = async (endpoint) => {
  try {
    const response = await fetch(`${API_BASE_URL}/${endpoint}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch ${endpoint}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`API Error (${endpoint}):`, error);
    return null;
  }
};

export const fetchContentBlocks = () => fetchData('contentBlocks');

export const fetchSubjectIndicators = () => fetchData('subjectIndicators');

export const fetchObjectIndicators = () => fetchData('objectIndicators');

export const fetchRelationsContentBlocks = () => fetchData('relationsContentBlocks');
