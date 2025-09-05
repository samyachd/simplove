from django.shortcuts import render
from django.http import HttpResponse

def profiles_view(request):
     return HttpResponse("Profiles.")