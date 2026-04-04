const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";

const parseErrorDetail = async (response, fallbackMessage) => {
  try {
    const payload = await response.json();
    if (payload?.detail) {
      return payload.detail;
    }
  } catch {
    // ignore json parsing errors and fallback to default message
  }
  return fallbackMessage;
};

export const fetchUploadIndicators = async () => {
  const response = await fetch(`${API_BASE_URL}/data/upload/indicators`, {
    method: "GET",
    headers: { Accept: "application/json" },
    cache: "no-store",
  });

  if (!response.ok) {
    const message = await parseErrorDetail(response, "Не удалось получить список показателей.");
    throw new Error(message);
  }

  return response.json();
};

export const uploadIndicatorFile = async ({ indicatorKey, file }) => {
  const formData = new FormData();
  formData.append("indicator_key", indicatorKey);
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/data/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const message = await parseErrorDetail(response, "Не удалось загрузить файл.");
    throw new Error(message);
  }

  return response.json();
};
