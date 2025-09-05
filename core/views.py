from django.shortcuts import render
from django.http import HttpResponse

def core_view(request):
     return HttpResponse("Home.")