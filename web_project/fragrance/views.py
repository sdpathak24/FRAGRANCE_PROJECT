from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Fragrance, Cart
from django.http import JsonResponse

def homePage(request):
    fragrance = Fragrance.objects.all()
    sections = ['Men', 'Women']
    return render(request, 'homePage.html', {'fragrance': fragrance, 'sections': sections})

def productsByCategory(request, category):
    filteredFragrances = Fragrance.objects.filter(category=category)

    sort = request.GET.get('sort')
    deals = request.GET.get('sale')
    brand = request.GET.get('brand')

    if sort == 'priceAsc':
        filteredFragrances = filteredFragrances.order_by('price')
    elif sort == 'priceDesc':
        filteredFragrances = filteredFragrances.order_by('-price')

    if deals == 'onSale':
        filteredFragrances = filteredFragrances.filter(isOnSale=True)

    if brand:
        filteredFragrances = filteredFragrances.filter(brand=brand)

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

def order(request, id):
    cart = request.session.get('cart', {})
    strId = str(id)
    product = Fragrance.objects.get(id=id)
    quantity = int(request.POST.get('quantity', 1))
    if strId in cart:
        cart[strId]['quantity'] += quantity
    else:
        cart[strId] = {
            'name': product.name,
            'price': product.price,
            'salePrice': product.salePrice,
            'quantity': quantity,
            'isOnSale': product.isOnSale,
            'img': product.img,
        }
    request.session['cart'] = cart
    return redirect('productsByCategory', category=product.category)

def cart(request):
    cart = request.session.get('cart', {})
    total = 0
    for item_id, item in cart.items():
        salePrice = item['salePrice']
        price = salePrice if salePrice else item['price']
        item['total'] = price * item['quantity']
        total += item['total']
    return render(request, 'cart.html', {'cart': cart, 'total':  total})

def updateCart(request, id):
    cart = request.session.get('cart', {})
    strId = str(id)
    if strId in cart:
        newQuantity = int(request.POST.get('quantity', 1))
        if newQuantity > 0:
            cart[strId]['quantity'] = newQuantity
        else:
            del cart[strId]
    request.session['cart'] = cart

    return redirect('cart')

def deleteFromCart(request, id):
    cart = request.session.get('cart', {})
    strId = str(id)
    if strId in cart:
        del cart[strId]
    request.session['cart'] = cart
    return redirect('cart')

def thankyou(request):
    return render(request, 'thankyou.html')

def clearCart(request):
    if request.method == 'POST':
        request.session['cart'] = {}
        return JsonResponse({'status': 'success', 'message': 'Cart cleared.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)