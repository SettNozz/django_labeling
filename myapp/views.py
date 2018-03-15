from django.shortcuts import render_to_response
from jinja2 import Template
from django.http import HttpResponse
from django.db import connection
from django.template import loader


def index(request):
    html = open("myapp/templates/start.html").read()
    template = Template(html)
    cursor = connection.cursor()
    sql_request = "SELECT DISTINCT submissions.picture FROM submissions WHERE submissions.description != 'water';"
    cursor.execute(sql_request)
    b = cursor.fetchmany(94                                                                                                                                     )
    c = []
    for i in b:
        c.append(str(''.join(i)))
    context = {'class_link': c}
    data = template.render(context)
    with open("myapp/templates/final_file.html", "wb") as fh:
        fh.write(data.encode())
    tp = "final_file.html"
    return render_to_response(tp)
