from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    # return HttpResponse('ola')
    return render(request, 'core/index.html')