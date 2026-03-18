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
    const response = await fetch(`${API_BASE_URL}/${endpoint}`, {
      method: 'GET',
      headers: {
        Accept: 'application/json'
      },
      cache: 'no-store'
    });
    if (!response.ok) {
      throw new Error(`Failed to fetch ${endpoint}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`API Error (${endpoint}):`, error);
    return null;
  }
};


import { CONTENT_BLOCKS } from '@/constants/contentBlocks';

export const fetchContentBlocks = async () => {
  const data = await fetchData('contentBlocks');
  return data && Object.keys(data).length ? data : CONTENT_BLOCKS;
};

import { SUBJECT_INDICATORS } from '@/constants/subjectIndicators';
import { OBJECT_INDICATORS } from '@/constants/objectIndicators';
import { RELATIONS } from '@/constants/relations';

export const fetchSubjectIndicators = async () => {
  const data = await fetchData('subjectIndicators');
  return data?.length ? data : SUBJECT_INDICATORS;
};

export const fetchObjectIndicators = async () => {
  const data = await fetchData('objectIndicators');
  return data?.length ? data : OBJECT_INDICATORS;
};

export const fetchRelationsContentBlocks = async () => {
  const data = await fetchData('relationsContentBlocks');
  return data && Object.keys(data).length ? data : RELATIONS;
};
