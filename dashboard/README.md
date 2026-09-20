# Vayu Dashboard (Synthetic Demo)

A responsive, dependency-free dashboard prototype for the AI-Powered Air Pollution Source Attribution Platform.

## Run locally

No Node.js build is required. From the repository root, open `dashboard/index.html` in a browser, or serve the repository with Python:

```powershell
python -m http.server 8000
```

Then visit `http://localhost:8000/dashboard/`.

## Included

- India overview with illustrative pollution markers
- AQI, PM2.5, PM10 and NO₂ selector
- National and regional filters
- Selectable city marker details
- Summary metrics, synthetic event feed, attribution contributions and illustrative forecast chart
- Responsive dark UI

## Important

All dashboard city values, map placement, event cards, and chart series are hardcoded illustrative demo data. The dashboard does not yet call the FastAPI backend or render a true GIS/geospatial heat surface. The map is a stylized SVG overview for prototyping the experience. Keep the synthetic-data label visible until real data and API integration are implemented.
