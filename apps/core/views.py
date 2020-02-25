from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.funcionarios.models import Funcionario

@login_required
def home(request):

    data = {}
    data['usuario'] = request.user
    return render(request, 'core/index.html', data)

def template(request):
    return render(request, 'index.html')

def sb_admin(request):
    return render(request, 'sb_admin/index.html')