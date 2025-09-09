from django.shortcuts import render

def home(request):
    return render(request, "core/index.html")
from django.http import HttpResponse

def core_view(request):
     return HttpResponse("Home.")
