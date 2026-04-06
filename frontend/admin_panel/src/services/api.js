const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";

const TABLE_ENDPOINTS = {
  regions: "regions",
  units: "units",
  indicator_subtypes: "indicator_subtypes",
  indicators: "indicators",
  data_sources: "data_sources",
  indicator_values: "indicator_values",
  population_age_sex: "population_age_sex",
  regional_programs: "regional_programs",
  program_regions: "program_regions",
  events: "events",
};

async function fetchApi(endpoint, options = {}) {
  const response = await fetch(`${API_BASE_URL}/${endpoint}`, {
    headers: {
      Accept: "application/json",
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${endpoint}`);
  }

  return response.json();
}

export const getTableChunk = async (tableKey, limit = 3, offset = 0) => {
  const endpoint = TABLE_ENDPOINTS[tableKey];
  if (!endpoint) {
    return [];
  }
  return fetchApi(`${endpoint}/get_chunk?limit=${limit}&offset=${offset}`);
};

export const getTableCount = async (tableKey) => {
  const endpoint = TABLE_ENDPOINTS[tableKey];
  if (!endpoint) {
    return 0;
  }
  return fetchApi(`${endpoint}/get_count`);
};

export const getTableCountFromChunks = async (tableKey, chunkSize = 500) => {
  let offset = 0;
  let total = 0;

  while (true) {
    const chunk = await getTableChunk(tableKey, chunkSize, offset);
    if (!Array.isArray(chunk) || chunk.length === 0) {
      break;
    }

    total += chunk.length;
    if (chunk.length < chunkSize) {
      break;
    }

    offset += chunkSize;
  }

  return total;
};

export const getUploadIndicators = async () => fetchApi("data/upload/indicators");

export const uploadDataFile = async ({ file, indicatorKey }) => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("indicator_key", indicatorKey);

  return fetchApi("data/upload", {
    method: "POST",
    body: formData,
  });
};

export const deleteIndicatorValueById = async (id) =>
  fetchApi(`indicator_values/delete?id=${encodeURIComponent(String(id))}`, {
    method: "DELETE",
  });
