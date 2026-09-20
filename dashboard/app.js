(() => {
  const cities = [
    {name:'New Delhi',state:'Delhi',region:'north',x:340,y:224,aqi:289,pm25:178,pm10:252,no2:68},
    {name:'Jaipur',state:'Rajasthan',region:'north',x:286,y:270,aqi:198,pm25:104,pm10:190,no2:43},
    {name:'Lucknow',state:'Uttar Pradesh',region:'north',x:420,y:260,aqi:221,pm25:122,pm10:211,no2:52},
    {name:'Chandigarh',state:'Chandigarh',region:'north',x:327,y:170,aqi:156,pm25:76,pm10:143,no2:35},
    {name:'Srinagar',state:'Jammu & Kashmir',region:'north',x:277,y:112,aqi:92,pm25:39,pm10:82,no2:19},
    {name:'Ahmedabad',state:'Gujarat',region:'west',x:220,y:337,aqi:164,pm25:81,pm10:157,no2:39},
    {name:'Mumbai',state:'Maharashtra',region:'west',x:286,y:410,aqi:133,pm25:61,pm10:128,no2:32},
    {name:'Pune',state:'Maharashtra',region:'west',x:315,y:430,aqi:119,pm25:54,pm10:113,no2:27},
    {name:'Bhopal',state:'Madhya Pradesh',region:'central',x:390,y:337,aqi:174,pm25:87,pm10:166,no2:40},
    {name:'Kolkata',state:'West Bengal',region:'east',x:534,y:335,aqi:203,pm25:111,pm10:202,no2:48},
    {name:'Patna',state:'Bihar',region:'east',x:487,y:292,aqi:218,pm25:119,pm10:207,no2:51},
    {name:'Bhubaneswar',state:'Odisha',region:'east',x:492,y:394,aqi:127,pm25:58,pm10:121,no2:29},
    {name:'Hyderabad',state:'Telangana',region:'south',x:408,y:425,aqi:141,pm25:67,pm10:134,no2:33},
    {name:'Bengaluru',state:'Karnataka',region:'south',x:365,y:485,aqi:108,pm25:48,pm10:104,no2:24},
    {name:'Chennai',state:'Tamil Nadu',region:'south',x:445,y:482,aqi:126,pm25:57,pm10:119,no2:30},
    {name:'Kochi',state:'Kerala',region:'south',x:333,y:525,aqi:78,pm25:32,pm10:72,no2:17}
  ];
  const events = [
    {id:'EVT-G042-01',city:'Delhi NCR',time:'Today · 19:00',level:'critical',value:289,source:'Traffic'},
    {id:'EVT-G018-04',city:'Patna urban grid',time:'Today · 17:00',level:'critical',value:218,source:'Mixed urban'},
    {id:'EVT-G027-02',city:'Kolkata east',time:'Today · 15:00',level:'high',value:203,source:'Traffic'},
    {id:'EVT-G033-08',city:'Jaipur central',time:'Today · 13:00',level:'high',value:198,source:'Road dust'},
    {id:'EVT-G011-03',city:'Bhopal central',time:'Today · 11:00',level:'moderate',value:174,source:'Mixed urban'}
  ];
  const $ = id => document.getElementById(id);
  const pollutant = $('pollutant'), viewMode = $('viewMode'), markers = $('cityMarkers');
  const valueOf = city => Number(city[pollutant.value]);
  const colorOf = value => value <= 50 ? '#5dd5a1' : value <= 100 ? '#e5d66b' : value <= 150 ? '#f4b35f' : value <= 200 ? '#f18b63' : '#fa6879';
  const statusOf = value => value <= 50 ? 'Good' : value <= 100 ? 'Satisfactory' : value <= 150 ? 'Moderate' : value <= 200 ? 'Poor' : 'Severe';
  const unitOf = () => pollutant.value === 'aqi' ? 'AQI' : 'µg/m³';
  const visibleCities = () => cities.filter(c => viewMode.value === 'national' || c.region === viewMode.value);

  function renderMap() {
    const visible = visibleCities();
    markers.innerHTML = visible.map(c => {
      const value = valueOf(c), color = colorOf(value), r = Math.max(7, Math.min(15, 6 + value / 35));
      return `<g class="city-marker" tabindex="0" role="button" aria-label="Select ${c.name}, ${value} ${unitOf()}" data-city="${c.name}"><circle class="halo" cx="${c.x}" cy="${c.y}" r="${r+8}" fill="${color}" filter="url(#glow)"/><circle class="core" cx="${c.x}" cy="${c.y}" r="${r}" fill="${color}"/><text x="${c.x+12}" y="${c.y+4}">${c.name}</text></g>`;
    }).join('');
    markers.querySelectorAll('.city-marker').forEach(el => {
      const select = () => selectCity(cities.find(c => c.name === el.dataset.city));
      el.addEventListener('click', select);
      el.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); select(); } });
      el.addEventListener('mouseenter', e => { const c = cities.find(x => x.name === el.dataset.city); const tip = $('mapTooltip'); tip.innerHTML = `<strong>${c.name}</strong><br>${valueOf(c)} ${unitOf()} · ${statusOf(valueOf(c))}`; tip.hidden = false; const rect = $('indiaMap').getBoundingClientRect(); tip.style.left = `${Math.min(rect.width-150, c.x/760*rect.width+14)}px`; tip.style.top = `${Math.max(8,c.y/600*rect.height-10)}px`; });
      el.addEventListener('mouseleave', () => $('mapTooltip').hidden = true);
    });
    $('cityCount').textContent = visible.length;
    $('avgAqi').innerHTML = `${Math.round(visible.reduce((sum,c)=>sum+valueOf(c),0)/visible.length)} <small>${unitOf()}</small>`;
    if (!visible.some(c => c.name === $('selectedName').textContent)) selectCity(visible[0]);
  }
  function selectCity(city) {
    if (!city) return;
    const value = valueOf(city), color = colorOf(value);
    $('selectedName').textContent = city.name;
    $('selectedMeta').textContent = `${city.state} · Synthetic demo station`;
    $('selectedValue').textContent = value;
    $('selectedUnit').textContent = unitOf();
    $('selectedStatus').textContent = statusOf(value);
    $('selectedStatus').className = `aqi-status ${value>200?'severe-text':''}`;
    $('selectedColor').style.background = color;
  }
  function renderEvents() {
    $('eventList').innerHTML = events.map(e => `<div class="event-row"><i class="event-mark event-${e.level}"></i><div class="event-main"><strong>${e.city}</strong><span>${e.id} · ${e.time} · ${e.source}</span></div><div class="event-value"><strong>${e.value}</strong><span>AQI · ${e.level}</span></div></div>`).join('');
  }
  function renderChart() {
    const observed = [96,108,101,124,113,139,127,152,141,174,158,189,166,202,178,191,169,183];
    const forecast = [183,176,169,162,154,147,143,139];
    const all = observed.concat(forecast), W=720,H=205,L=34,R=12,T=10,B=24, max=250;
    const x=i=>L+i/(all.length-1)*(W-L-R), y=v=>T+(max-v)/max*(H-T-B);
    const path=arr=>arr.map((v,i)=>`${i?'L':'M'}${x(i).toFixed(1)},${y(v).toFixed(1)}`).join(' ');
    const area=`${path(observed)} L${x(observed.length-1)},${H-B} L${x(0)},${H-B} Z`;
    const grid=[50,100,150,200].map(v=>`<line x1="${L}" y1="${y(v)}" x2="${W-R}" y2="${y(v)}" stroke="#26374b" stroke-dasharray="3 5"/><text x="${L-8}" y="${y(v)+3}" text-anchor="end" fill="#72839a" font-size="10">${v}</text>`).join('');
    const forecastPath=forecast.map((v,i)=>`${i?'L':'M'}${x(observed.length-1+i)},${y(v)}`).join(' ');
    $('trendChart').innerHTML=`<svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="none" aria-label="Synthetic observed AQI and forecast"><defs><linearGradient id="chartFill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#62d7d0" stop-opacity=".22"/><stop offset="1" stop-color="#62d7d0" stop-opacity="0"/></linearGradient></defs>${grid}<path d="${area}" fill="url(#chartFill)"/><path d="${path(observed)}" fill="none" stroke="#62d7d0" stroke-width="2.5" stroke-linecap="round"/><path d="${forecastPath}" fill="none" stroke="#b69bea" stroke-width="2.5" stroke-dasharray="6 5" stroke-linecap="round"/><line x1="${x(observed.length-1)}" y1="${T}" x2="${x(observed.length-1)}" y2="${H-B}" stroke="#71819a" stroke-dasharray="3 4"/><text x="${x(observed.length-1)+7}" y="${T+12}" fill="#a9b7c9" font-size="9">NOW</text></svg>`;
  }
  pollutant.addEventListener('change', () => { renderMap(); renderChart(); });
  viewMode.addEventListener('change', renderMap);
  $('resetMap').addEventListener('click', () => { viewMode.value='national'; pollutant.value='aqi'; renderMap(); renderChart(); });
  $('refreshBtn').addEventListener('click', () => { $('updatedAt').textContent = new Date().toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'}); $('refreshBtn').classList.add('spinning'); setTimeout(()=>$('refreshBtn').classList.remove('spinning'),350); });
  $('showAllEvents').addEventListener('click', () => { $('eventList').innerHTML = events.concat([{id:'EVT-G014-06',city:'Ahmedabad west',time:'Today · 09:00',level:'moderate',value:164,source:'Road dust'},{id:'EVT-G031-01',city:'Mumbai central',time:'Today · 07:00',level:'moderate',value:133,source:'Traffic'}]).map(e=>`<div class="event-row"><i class="event-mark event-${e.level}"></i><div class="event-main"><strong>${e.city}</strong><span>${e.id} · ${e.time} · ${e.source}</span></div><div class="event-value"><strong>${e.value}</strong><span>AQI · ${e.level}</span></div></div>`).join(''); $('showAllEvents').textContent='Showing all'; });
  renderMap(); renderEvents(); renderChart();
})();
