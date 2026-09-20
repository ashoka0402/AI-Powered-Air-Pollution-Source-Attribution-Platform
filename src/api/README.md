# VAYU Person 3 API

## Run locally

From the repository root, activate your venv and install dependencies:

```bash
pip install -r requirements.txt
uvicorn src.api.main:app --reload
```

- API: `http://127.0.0.1:8000`
- Interactive OpenAPI docs: `http://127.0.0.1:8000/docs`
- Health: `GET /api/v1/health`

## Endpoints

| Method | Route | Purpose |
|---|---|---|
| GET | `/api/v1/pollution/current` | Current demo readings; optional `city`, `pollutant` |
| GET | `/api/v1/pollution/history` | Time-series demo history |
| GET | `/api/v1/events` | Filterable event list |
| GET | `/api/v1/events/{event_id}` | Event details and evidence notes |
| GET | `/api/v1/events/{event_id}/attribution` | Probable source probabilities and confidence |
| GET | `/api/v1/exposure/{city}` | Exposure endpoint; population/grid calculations explicitly pending |
| GET | `/api/v1/recommendations/{event_id}` | Rule-based decision-support suggestions |
| POST | `/api/v1/citizen-reports` | Validate and submit a citizen report |
| GET | `/api/v1/citizen-reports` | List reports held in process memory |

`dashboard/api.js` exposes the canonical browser methods through `window.VayuAPI`. Load it after configuration and before calling those methods.

## Integration status and limitations

This is a working API contract/demo implementation, not live monitoring. Responses are labeled `synthetic_demo`; citizen reports are stored in memory and disappear on restart. Exposure population estimates and sensitive-location results are not fabricated: they remain unavailable until validated neighbourhood grids and population/sensitive-place data are connected. Recommendation rules are suggestions requiring human review. The next integration step is to replace the demo fixtures with Person 1's PostGIS repositories and Person 2's attribution/forecast services without changing the canonical routes.
