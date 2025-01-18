from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
# Importe requests y json
import requests
import json
 # Importe el decorador login_required
from django.contrib.auth.decorators import login_required, permission_required

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
     responses = response_dict.values()


     print("Endpoint ", url)
     print("Response ", response_dict)

     # Respuestas totales
     total_responses = len(response_dict.keys())

    # Objeto con los datos a renderizar
     data = {
         'title': 'Landing - Dashboard',
         'total_responses': total_responses,
         'responses': responses

     }


     # Renderización en la plantilla
     return render(request, 'main/index.html', data)
