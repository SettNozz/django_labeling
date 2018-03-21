from django.http import HttpResponse
from django.db import connection
from django.template import loader


def index(request):
    cursor = connection.cursor()
    sql_request = "SELECT DISTINCT submissions.picture, submissions.description from submissions WHERE submissions.picture != '' AND submissions.picture != 'Empty' AND submissions.picture != 'water' AND submissions.description != '';"
    cursor.execute(sql_request)
    b = cursor.fetchall()
    context = {'class_link': b}
    template = loader.get_template("myapp/start.html")
    return HttpResponse(template.render(context, request))


def loaders(request):
    name = request.GET.get('a')
    return HttpResponse(f"Hello, {name}")
