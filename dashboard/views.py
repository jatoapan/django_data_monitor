from django.shortcuts import render
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta

# Create your views here.
def dashboard(request):
    return render(request, 'dashboard/base.html')

@login_required
def index(request):
    response = requests.get(settings.API_URL)  # URL de la API
    posts = response.json()  # Convertir la respuesta a JSON

    total_responses = len(posts)
    metricas = obtener_metricas(posts)

    data = {
        'title': 'Landing Page Dashboard',
        **metricas
    }

    return render(request, 'dashboard/index.html', data)



def obtener_metricas(json):
    def obtener_ciudad(addr):
        ciudad = (addr).split(",")[0].strip()
        return ciudad

    rows = []
    for _id, row in json.items():
        r = dict(row)
        r["_id"] = _id
        rows.append(r)

    for r in rows:
        r["city"] = obtener_ciudad(r["address"])

    city_counts = Counter(r["city"] for r in rows if r.get("city"))
    top_city, top_city_count = ("—", 0)
    if city_counts:
        top_city, top_city_count = city_counts.most_common(1)[0]

    ECU = timezone(timedelta(hours=-5))
    for r in rows:
        r["dt"] = datetime.fromtimestamp(r["timestamp"]/1000, tz=timezone.utc).astimezone(ECU)

    latest_dt = max(r["dt"] for r in rows) if rows else None
    
    day_count = defaultdict(int)
    for r in rows:
        day_count[r["dt"].date()] += 1
    daily_counts = [{"date": d.isoformat(), "count": day_count[d]} for d in sorted(day_count)]

    data = {
        "total_responses": len(rows),
        "top_city": top_city,
        "top_city_count": top_city_count,
        "latest_request": latest_dt,     
        "rows": rows,                    
        "daily_counts": daily_counts,    
    }

    return data
