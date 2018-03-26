from django.http import HttpResponse
from django.db import connection
from django.template import loader
from django.shortcuts import render
from django.utils.safestring import mark_safe
import asyncio
import websockets
import json
import time


def index(request):
    cursor = connection.cursor()
    sql_request = "SELECT DISTINCT submissions.picture, submissions.description from submissions WHERE submissions.picture != '' AND submissions.picture != 'Empty' AND submissions.picture != 'water' AND submissions.description != '';"
    cursor.execute(sql_request)
    b = cursor.fetchall()
    context = {'class_link': b}
    template = loader.get_template("myapp/start.html")
    return HttpResponse(template.render(context, request))


def loaders(request, class_name):
    print(class_name)
    # name = request.GET.get('a')
    # sock_path = f'ws://127.0.0.1:8000/ws/loaders'

    return render(request, 'myapp/status_load.html', {
        'class_name_json': mark_safe(json.dumps(class_name))
    })