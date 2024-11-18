from django.shortcuts import render
from django.http import HttpResponse
from .models import Fragrance

def homePage(request):
    fragrance = Fragrance.objects.all()
    return render(request, 'homePage.html', {'fragrance': fragrance})
