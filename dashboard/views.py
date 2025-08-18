from django.shortcuts import render
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Create your views here.
def dashboard(request):
    return render(request, 'dashboard/base.html')

@login_required
def index(request):
    response = requests.get(settings.API_URL)  # URL de la API
    posts = response.json()  # Convertir la respuesta a JSON

    total_responses = len(posts)

    data = {
        'title': 'Landing Page Dashboard',
        'total_responses': total_responses,
    }

    return render(request, 'dashboard/index.html', data)


