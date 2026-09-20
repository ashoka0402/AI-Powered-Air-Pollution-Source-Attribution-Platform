/* Person 3 canonical frontend API services. Set window.VAYU_API_BASE before this file if needed. */
(() => {
  const BASE = (window.VAYU_API_BASE || "http://127.0.0.1:8000").replace(/\/$/, "");
  async function request(path, options = {}) {
    const response = await fetch(`${BASE}${path}`, {
      ...options,
      headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    });
    const body = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(body.detail || `API error ${response.status}`);
    return body;
  }
  window.VayuAPI = Object.freeze({
    fetchCurrentPollution: (city, pollutant = "aqi") => request(`/api/v1/pollution/current?${new URLSearchParams({ ...(city ? { city } : {}), pollutant })}`),
    fetchPollutionHistory: (city = "Delhi NCR", pollutant = "pm25", hours = 24) => request(`/api/v1/pollution/history?${new URLSearchParams({ city, pollutant, hours })}`),
    fetchPollutionEvents: (filters = {}) => request(`/api/v1/events?${new URLSearchParams(filters)}`),
    fetchEventDetails: (eventId) => request(`/api/v1/events/${encodeURIComponent(eventId)}`),
    fetchEventAttribution: (eventId) => request(`/api/v1/events/${encodeURIComponent(eventId)}/attribution`),
    fetchExposureData: (city) => request(`/api/v1/exposure/${encodeURIComponent(city)}`),
    fetchRecommendations: (eventId) => request(`/api/v1/recommendations/${encodeURIComponent(eventId)}`),
    submitCitizenReport: (report) => request("/api/v1/citizen-reports", { method: "POST", body: JSON.stringify(report) }),
    fetchCitizenReports: () => request("/api/v1/citizen-reports"),
  });
})();
