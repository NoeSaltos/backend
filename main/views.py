from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
import requests
import json
from collections import Counter
from datetime import datetime
from django.conf import settings

# Restricción de acceso con @login_required
@login_required
@permission_required('main.index_viewer', raise_exception=True)
def index(request):
    # Obtener URL base para construir el endpoint del API
    current_url = request.build_absolute_uri()
    url = current_url + '/api/v1/landing'

    try:
        # Petición al REST API
        response_http = requests.get(url, timeout=10)  # Tiempo de espera de 10s
        response_http.raise_for_status()  # Lanza un error si la respuesta no es 200 OK
        response_dict = response_http.json()  # Decodifica la respuesta JSON
    except requests.RequestException as e:
        return HttpResponse(f"Error al obtener datos del API: {e}", status=500)

    # Obtener valores de las respuestas
    responses = list(response_dict.values())

    if settings.DEBUG:  # Solo imprime logs si DEBUG está activado
        print("Endpoint:", url)
        print("Response:", response_dict)

    # Respuestas totales
    total_responses = len(response_dict)

    # Obtener la hora de la primera y última respuesta
    first_response_time = responses[0].get('saved', 'No disponible') if responses else 'No disponible'
    ultima_respuesta = responses[-1].get('saved', 'No disponible') if responses else 'No disponible'

    # Contar respuestas por día
    dates = []
    for response in responses:
        saved_time = response.get('saved', '').replace('\xa0', ' ').replace('a. m.', 'AM').replace('p. m.', 'PM')
        try:
            date = datetime.strptime(saved_time, "%d/%m/%Y, %I:%M:%S %p").strftime("%d/%m/%Y")
            dates.append(date)
        except ValueError:
            if settings.DEBUG:
                print(f"Error parsing date: {saved_time}")

    # Convertir a diccionario estándar para JSON
    date_counts = dict(Counter(dates))

    # Determinar el día con más respuestas
    most_common_day, most_common_day_count = ('No disponible', 0)
    if date_counts:
        most_common_day, most_common_day_count = max(date_counts.items(), key=lambda x: x[1])

    # if settings.DEBUG:
    #     print("Dates:", dates)
    #     print("Date Counts:", date_counts)
    #     print("Most Common Day:", most_common_day)
    #     print("Most Common Day Count:", most_common_day_count)

    # Datos a renderizar en la plantilla
    data = {
        'title': 'Landing - Dashboard',
        'total_responses': total_responses,
        'responses': responses,
        'first_response_time': first_response_time,
        'ultima_respuesta': ultima_respuesta,
        'most_common_day': most_common_day,
        'most_common_day_count': most_common_day_count,
        'date_counts': json.dumps(date_counts, ensure_ascii=False),  # Convierte a JSON
    }

    return render(request, 'main/index.html', data)
