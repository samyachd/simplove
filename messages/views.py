from django.shortcuts import render
from django.http import HttpResponse

def messages_view(request):
     return HttpResponse("Messages.")
    
