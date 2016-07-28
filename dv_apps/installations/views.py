from django.shortcuts import render

# Create your views here.
from django.template import loader
from .models import Installation, Institution
from django.http import Http404
from django.http import HttpResponse

def Map(request):
    install_list = Installation.objects.all()
    arr = []
    
    for i  in install_list:
        lists = Institution.objects.filter(host__name=i.name)
        arr.append(lists)
    
    d = dict(
        install_list = install_list,
        arr = arr,
    )
    
    return render(request, 'installations/map.html', d)
    