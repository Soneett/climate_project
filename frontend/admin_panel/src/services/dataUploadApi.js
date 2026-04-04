const API_BASE_URL = import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, "") || "";

function buildUrl(path) {
  if (!API_BASE_URL) {
    return path;
  }
  return `${API_BASE_URL}${path}`;
}

async function parseResponse(response) {
  const payload = await response.json().catch(() => null);
  if (response.ok) {
    return payload;
  }

  const detail = payload?.detail;
  const errorMessage =
    typeof detail === "string"
      ? detail
      : "Не удалось выполнить запрос к сервису загрузки данных.";

  throw new Error(errorMessage);
}

export async function getUploadIndicators() {
  const response = await fetch(buildUrl("/api/data/upload/indicators"));
  const payload = await parseResponse(response);
  return Array.isArray(payload) ? payload : [];
}

export async function uploadIndicatorData({ file, indicatorKey }) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("indicator_key", indicatorKey);

  const response = await fetch(buildUrl("/api/data/upload"), {
    method: "POST",
    body: formData,
  });

  return parseResponse(response);
}
