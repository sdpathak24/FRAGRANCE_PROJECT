from django.shortcuts import render
from django.http import HttpResponse
from .models import Fragrance
from django.http import JsonResponse

def homePage(request):
    fragrance = Fragrance.objects.all()
    sections = ['Men', 'Women']
    return render(request, 'homePage.html', {'fragrance': fragrance, 'sections': sections})

def productsByCategory(request, category):
    filteredFragrances = Fragrance.objects.filter(category=category)

    sort = request.GET.get('sort')
    deals = request.GET.get('sale')

    if sort == 'priceAsc':
        filteredFragrances = filteredFragrances.order_by('price')
    elif sort == 'priceDesc':
        filteredFragrances = filteredFragrances.order_by('-price')

    if deals == 'onSale':
        filteredFragrances = filteredFragrances.filter(isOnSale=True)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'fragrance': [
                {
                    'name': frag.name,
                    'price': frag.price,
                    'salePrice': frag.salePrice,
                    'img': frag.img,
                    'isOnSale': frag.isOnSale
                }
                for frag in filteredFragrances
            ]
        }
        return JsonResponse(data)
    return render(request, 'productsByCategory.html', {'fragrance': filteredFragrances, 'category': category})

def aboutPage(request):
    return render(request, 'about.html')

