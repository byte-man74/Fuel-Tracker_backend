from django.shortcuts import render

# Create your views here.

def add_fueling_station (request):
    return render (request, 'main/form.html')