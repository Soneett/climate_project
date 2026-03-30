const API_BASE_URL = 'http://localhost:3001';

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
