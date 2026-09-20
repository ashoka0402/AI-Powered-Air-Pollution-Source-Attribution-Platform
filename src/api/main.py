"""Person 3 API layer for the VAYU dashboard.

Deterministic synthetic demo fixtures by default. Replace these with the
Person 1 repository and Person 2 pipeline adapter for production.
"""
from __future__ import annotations
from datetime import datetime, timedelta, timezone
from typing import Literal
from uuid import uuid4
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="VAYU Air Intelligence API", version="1.0.1", description="Person 3 API; fixtures are synthetic demo data.")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"])

CITY_DATA = [
 {"city":"Delhi NCR","state":"Delhi","latitude":28.6139,"longitude":77.2090,"aqi":178,"pm25":92,"pm10":164,"no2":41,"status":"Poor"},
 {"city":"Mumbai","state":"Maharashtra","latitude":19.0760,"longitude":72.8777,"aqi":112,"pm25":48,"pm10":91,"no2":28,"status":"Moderate"},
 {"city":"Pune","state":"Maharashtra","latitude":18.5204,"longitude":73.8567,"aqi":86,"pm25":31,"pm10":62,"no2":19,"status":"Moderate"},
 {"city":"Ahmedabad","state":"Gujarat","latitude":23.0225,"longitude":72.5714,"aqi":129,"pm25":57,"pm10":105,"no2":33,"status":"Poor"},
 {"city":"Bengaluru","state":"Karnataka","latitude":12.9716,"longitude":77.5946,"aqi":74,"pm25":26,"pm10":49,"no2":17,"status":"Moderate"},
 {"city":"Hyderabad","state":"Telangana","latitude":17.3850,"longitude":78.4867,"aqi":91,"pm25":34,"pm10":66,"no2":21,"status":"Moderate"},
 {"city":"Chennai","state":"Tamil Nadu","latitude":13.0827,"longitude":80.2707,"aqi":68,"pm25":23,"pm10":43,"no2":15,"status":"Moderate"},
 {"city":"Kolkata","state":"West Bengal","latitude":22.5726,"longitude":88.3639,"aqi":121,"pm25":53,"pm10":98,"no2":30,"status":"Poor"},
 {"city":"Lucknow","state":"Uttar Pradesh","latitude":26.8467,"longitude":80.9462,"aqi":153,"pm25":77,"pm10":137,"no2":36,"status":"Poor"},
 {"city":"Jaipur","state":"Rajasthan","latitude":26.9124,"longitude":75.7873,"aqi":118,"pm25":51,"pm10":96,"no2":25,"status":"Poor"},
 {"city":"Bhopal","state":"Madhya Pradesh","latitude":23.2599,"longitude":77.4126,"aqi":99,"pm25":39,"pm10":73,"no2":22,"status":"Moderate"},
 {"city":"Chandigarh","state":"Chandigarh","latitude":30.7333,"longitude":76.7794,"aqi":104,"pm25":43,"pm10":82,"no2":24,"status":"Moderate"},
 {"city":"Patna","state":"Bihar","latitude":25.5941,"longitude":85.1376,"aqi":166,"pm25":84,"pm10":149,"no2":39,"status":"Poor"},
 {"city":"Indore","state":"Madhya Pradesh","latitude":22.7196,"longitude":75.8577,"aqi":88,"pm25":33,"pm10":63,"no2":20,"status":"Moderate"},
 {"city":"Kochi","state":"Kerala","latitude":9.9312,"longitude":76.2673,"aqi":56,"pm25":18,"pm10":36,"no2":12,"status":"Good"},
 {"city":"Guwahati","state":"Assam","latitude":26.1445,"longitude":91.7362,"aqi":107,"pm25":45,"pm10":86,"no2":23,"status":"Moderate"},
]
SOURCES = [{"source_type":s,"probability":p,"contribution":p} for s,p in [("traffic",.36),("construction",.17),("industrial",.12),("road_dust",.09),("other",.26)]]
EVENTS = [
 {"event_id":"EVT-DEL-001","city":"Delhi NCR","pollutant":"PM2.5","observed_value":92,"baseline_value":48,"severity":"high","status":"active","primary_source_type":"traffic","confidence":.53},
 {"event_id":"EVT-AHM-002","city":"Ahmedabad","pollutant":"PM10","observed_value":105,"baseline_value":61,"severity":"moderate","status":"active","primary_source_type":"construction","confidence":.48},
 {"event_id":"EVT-MUM-003","city":"Mumbai","pollutant":"PM2.5","observed_value":48,"baseline_value":29,"severity":"moderate","status":"active","primary_source_type":"traffic","confidence":.51},
]
REPORTS: list[dict] = []

class CitizenReportIn(BaseModel):
 latitude: float = Field(ge=-90, le=90)
 longitude: float = Field(ge=-180, le=180)
 category: Literal["smoke","dust","burning","odor","other"]
 description: str = Field(min_length=5,max_length=1000)
 image_url: str | None = None
class CitizenReportOut(CitizenReportIn):
 report_id: str
 timestamp: datetime
 credibility_score: float = .5
 status: str = "submitted"

def _city(city: str):
 found=next((x for x in CITY_DATA if x["city"].casefold()==city.casefold()),None)
 if not found: raise HTTPException(404,f"Unknown city: {city}")
 return found
def _event(event_id: str):
 found=next((e for e in EVENTS if e["event_id"]==event_id),None)
 if not found: raise HTTPException(404,"Event not found")
 return found

@app.get("/", tags=["service"])
def root():
 """Service landing response; interactive API documentation is at /docs."""
 return {"service":"VAYU Air Intelligence API","status":"ok","data_mode":"synthetic_demo","docs":"/docs","openapi":"/openapi.json","health":"/api/v1/health","api_prefix":"/api/v1"}
@app.get("/api/v1/health", tags=["service"])
def health(): return {"status":"ok","service":"vayu-api","data_mode":"synthetic_demo"}
@app.get("/api/v1/pollution/current")
def get_current_pollution(city: str|None=None,pollutant: Literal["aqi","pm25","pm10","no2"]="aqi"):
 rows=[_city(city)] if city else CITY_DATA
 return {"data_mode":"synthetic_demo","pollutant":pollutant,"units":"AQI" if pollutant=="aqi" else "µg/m³","readings":[{**r,"value":r[pollutant],"timestamp":datetime.now(timezone.utc).isoformat()} for r in rows]}
@app.get("/api/v1/pollution/history")
def get_pollution_history(city: str="Delhi NCR",pollutant: Literal["aqi","pm25","pm10","no2"]="pm25",hours: int=Query(24,ge=1,le=168)):
 current=_city(city)[pollutant]; now=datetime.now(timezone.utc)
 return {"data_mode":"synthetic_demo","city":city,"pollutant":pollutant,"points":[{"timestamp":(now-timedelta(hours=hours-i)).isoformat(),"value":round(max(0,current*(.78+.22*((i%7)/6))),1)} for i in range(hours+1)]}
@app.get("/api/v1/events")
def get_pollution_events(status: str|None=None,city: str|None=None):
 rows=EVENTS
 if status: rows=[e for e in rows if e["status"]==status]
 if city: rows=[e for e in rows if e["city"].casefold()==city.casefold()]
 return {"data_mode":"synthetic_demo","count":len(rows),"events":rows}
@app.get("/api/v1/events/{event_id}")
def get_event_details(event_id: str):
 event=_event(event_id)
 return {"data_mode":"synthetic_demo","event":event,"detected_at":datetime.now(timezone.utc).isoformat(),"evidence":["Concentration above demo baseline","Spatial candidate score available","Weather evidence not connected to a live provider"]}
@app.get("/api/v1/events/{event_id}/attribution")
def get_event_attribution(event_id: str):
 event=_event(event_id)
 return {"data_mode":"synthetic_demo","event_id":event_id,"primary_source_type":event["primary_source_type"],"confidence":event["confidence"],"model_version":"demo-v1","contributions":SOURCES,"caveat":"Probable attribution, not confirmed causation."}
@app.get("/api/v1/exposure/{city}")
def get_neighbourhood_exposure(city: str):
 c=_city(city); aqi=c["aqi"]; band="high" if aqi>150 else "moderate" if aqi>100 else "low"
 return {"data_mode":"synthetic_demo","city":city,"exposure_band":band,"estimated_exposed_population":None,"population_estimate_status":"not_computed_no_population_grid","sensitive_locations":[],"message":"Connect validated neighbourhood concentration and population grids to calculate these fields."}
@app.get("/api/v1/recommendations/{event_id}")
def get_event_recommendations(event_id: str):
 event=_event(event_id)
 actions={"traffic":["Review congestion management near the affected area","Check public-transport and idling-reduction measures"],"construction":["Inspect active construction dust controls","Verify site covering and water-suppression practices"],"industrial":["Review nearby facility operating and emissions records","Arrange targeted inspection where authorized"],"road_dust":["Assess road-cleaning and dust-suppression needs","Inspect unpaved shoulders and high-dust segments"]}.get(event["primary_source_type"],["Review local source and meteorological evidence"])
 return {"data_mode":"synthetic_demo","event_id":event_id,"recommendations":[{"action":a,"basis":"rule_based_demo","priority":"review"} for a in actions],"note":"Decision-support suggestions; require human and agency validation."}
@app.post("/api/v1/citizen-reports",response_model=CitizenReportOut,status_code=201)
def submit_citizen_report(payload: CitizenReportIn):
 report={**payload.model_dump(),"report_id":f"CR-{uuid4().hex[:10].upper()}","timestamp":datetime.now(timezone.utc),"credibility_score":.5,"status":"submitted"}; REPORTS.append(report); return report
@app.get("/api/v1/citizen-reports")
def list_citizen_reports(): return {"count":len(REPORTS),"reports":REPORTS,"data_mode":"in_memory_demo"}
