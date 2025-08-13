from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import requests
from django.conf import settings
from datetime import datetime
from collections import defaultdict
import json

def index(request):
    response = requests.get(settings.API_URL) 
    posts = response.json()
    total_responses = len(posts)
    now = datetime.now()
    month_responses = 0
    week_responses = 0
    today_responses = 0
    for p in posts.values():
        dt = datetime.fromtimestamp(int(p["timestamp"]) / 1000)
        if dt.year == now.year and dt.month == now.month:
            month_responses += 1
        if dt.isocalendar()[1] == now.isocalendar()[1] and dt.year == now.year:
            week_responses += 1
        if dt.date() == now.date():
            today_responses += 1
    chart_data = get_chart_data(posts)
    data = {
        'title': "Landing Page' Dashboard",
        'total_responses': total_responses,
        'month_responses': month_responses,
        'week_responses': week_responses,
        'today_responses': today_responses,
        'topics': get_users_topics(posts),
        'chart_data': json.dumps(chart_data)
    }
    return render(request, 'dashboard/index.html', data)

def dashboard(request):
    # return HttpResponse("¡Bienvenido a la aplicación Django!")
    return render(request, 'dashboard/base.html')

def get_users_topics(response):
    return [{'name': element['name'], 'topic': element['topic']} for element in response.values()]

def get_chart_data(response):
    daily_counts = defaultdict(int)
    for post in response.values():
        dt = datetime.fromtimestamp(int(post["timestamp"]) / 1000)
        date_str = dt.strftime('%Y-%m-%d')
        daily_counts[date_str] += 1
    sorted_dates = sorted(daily_counts.keys())[:] if daily_counts else []
    labels = []
    daily_data = []
    cumulative_data = []
    cumulative_total = 0
    for date_str in sorted_dates:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        labels.append(dt.strftime('%d/%m'))
        daily_count = daily_counts[date_str]
        daily_data.append(daily_count)
        cumulative_total += daily_count
        cumulative_data.append(cumulative_total)
    chart_config = {
        'labels': labels if labels else ['Sin datos'],
        'datasets': [
            {
                'label': 'Registros diarios',
                'data': daily_data if daily_data else [0],
                'backgroundColor': '#0694a2',
                'borderColor': '#0694a2',
            },
            {
                'label': 'Acumulado',
                'data': cumulative_data if cumulative_data else [0],
                'backgroundColor': '#7e3af2',
                'borderColor': '#7e3af2',
            }
        ]
    }
    return chart_config