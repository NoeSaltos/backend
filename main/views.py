from django.shortcuts import render
 # Importe el decorador login_required
from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.
from django.http import HttpResponse
# Importe requests y json
import requests
import json
from collections import Counter
from datetime import datetime


 # Restricción de acceso con @login_required
@login_required
@permission_required('main.index_viewer', raise_exception=True)

def index(request):
    #  return HttpResponse("Hello, World!")
    #  return render(request, 'main/base.html')
    # return render(request, 'main/index.html')
    # Arme el endpoint del REST API
     current_url = request.build_absolute_uri()
     url = current_url + '/api/v1/landing'

     # Petición al REST API
     response_http = requests.get(url)
     response_dict = json.loads(response_http.content)
     
     # Valores de la respuesta
     responses = list(response_dict.values())


     print("Endpoint ", url)
     print("Response ", response_dict)


     # Respuestas totales
     total_responses = len(response_dict.keys())

    # Obtener la hora de la primera respuesta
     first_response_time = 'No disponible'
     ultima_respuesta = 'No disponible'
     if responses:
        first_response_time = responses[0].get('saved', 'No disponible')
        ultima_respuesta = responses[-1].get('saved', 'No disponible')
    
     # Contar respuestas por día
     dates = []
     for response in responses:
         saved_time = response['saved'].replace('\xa0', ' ').replace('a. m.', 'AM').replace('p. m.', 'PM')
         print(f"Processing saved_time: {saved_time}")  # Agregar depuración
         try:
            date = datetime.strptime(saved_time, "%d/%m/%Y, %I:%M:%S %p").strftime("%d/%m/%Y")
            dates.append(date)
         except ValueError:
            print(f"Error parsing date: {saved_time}")

     date_counts = Counter(dates)
     if date_counts:
        most_common_day, most_common_day_count = date_counts.most_common(1)[0]
     else:
        most_common_day, most_common_day_count = 'No disponible', 0
     
     print("Dates: ", dates)
     print("Date Counts: ", date_counts)
     print("Most Common Day: ", most_common_day)
     print("Most Common Day Count: ", most_common_day_count)

    # Objeto con los datos a renderizar
     data = {
         'title': 'Landing - Dashboard',
         'total_responses': total_responses,
         'responses': responses,
         'first_response_time': first_response_time,
         'ultima_respuesta': ultima_respuesta,
         'most_common_day': most_common_day,
         'most_common_day_count': most_common_day_count

     }


     # Renderización en la plantilla
     return render(request, 'main/index.html', data)
