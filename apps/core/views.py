from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import sqlite3

print(sqlite3.sqlite_version)

@login_required
def home(request):

    data = {}
    data['usuario'] = request.user
    return render(request, 'core/index.html', data)

def template(request):
    return render(request, 'index.html')

