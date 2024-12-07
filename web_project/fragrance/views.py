from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Fragrance, Cart
from django.http import JsonResponse
from django.db.models import F, Value
from django.db.models.functions import Coalesce

def homePage(request):
    if 'username' not in request.session:
        return redirect('login')  # Redirect to login page
    fragrance = Fragrance.objects.all()
    sections = ['Men', 'Women']
    men_products = Fragrance.objects.filter(category='Men').order_by('-id')[:7]
    women_products = Fragrance.objects.filter(category='Women').order_by('-id')[:7]
    return render(request, 'homePage.html', {
        'fragrance': fragrance, 
        'sections': sections, 
        'men_products': men_products,
        'women_products': women_products
    })


def productsByCategory(request, category):
    if 'username' not in request.session:
        return redirect('login')
    filteredFragrances = Fragrance.objects.filter(category=category)

    name = request.GET.get('name')
    sort = request.GET.get('sort')
    deals = request.GET.get('sale')
    brand = request.GET.get('brand')

    if name:
        filteredFragrances = filteredFragrances.filter(name__icontains=name)

    if sort == 'priceAsc':
        filteredFragrances = filteredFragrances.annotate(effective_price=Coalesce('salePrice', 'price')).order_by('effective_price')
    elif sort == 'priceDesc':
        filteredFragrances = filteredFragrances.annotate(effective_price=Coalesce('salePrice', 'price')).order_by('-effective_price')

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
                    'isOnSale': frag.isOnSale,
                    'brand': frag.brand
                }
                for frag in filteredFragrances
            ]
        }
        return JsonResponse(data)
    return render(request, 'productsByCategory.html', {'fragrance': filteredFragrances, 'category': category})

def aboutPage(request):
    if 'username' not in request.session:
        return redirect('login') 
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
    if 'username' not in request.session:
        return redirect('login')  # Redirect to login page
    cart = request.session.get('cart', {})
    total = 0
    for item_id, item in cart.items():
        salePrice = item['salePrice']
        price = salePrice if salePrice else item['price']
        img = item['img']
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
    # You can process the payment here and clear the cart if needed
    if request.method == "POST":
        # Simulate successful payment processing
        # For now, let's assume payment is always successful
        request.session['cart'] = {}  # Clear the cart after successful payment

        return JsonResponse({'status': 'success'})
    return render(request, 'thankyou.html')

def clearCart(request):
    if 'cart' in request.session:
        del request.session['cart'] 
    return redirect('thankyou')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Dummy authentication
        if username == 'admin' and password == 'password':
            request.session['username'] = username
            return redirect('homePage')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials', 'hide_navbar': True})

    return render(request, 'login.html', {'hide_navbar': True})


# Logout view
def logout(request):
    request.session.flush()
    return redirect('login')


def some_protected_view(request):
    if 'username' not in request.session:
        return redirect('login')  # Redirect to login if not logged in

    # Normal view logic here
    return render(request, 'protected_page.html')