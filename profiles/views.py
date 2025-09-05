from django.shortcuts import render


# Create your views here.
def profile_views(request):
    context = {"nom": "Ayoub"}
    return render(request, "profiles/index.html", context)
