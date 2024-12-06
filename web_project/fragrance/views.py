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
        return redirect('login')  # Redirect to login page
    filteredFragrances = Fragrance.objects.filter(category=category)

    sort = request.GET.get('sort')
    deals = request.GET.get('sale')
    brand = request.GET.get('brand')

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
        return redirect('login')  # Redirect to login page
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
    if 'cart' in request.session:
        del request.session['cart']  # Clear the cart from the session
    
    # Redirect to the thank you page after clearing the cart
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


# from django.shortcuts import render
# from .models import Fragrance  # Ensure your Fragrance model is imported

# def homePage(request):
#     men_products = Fragrance.objects.filter(category='Men').order_by('-id')[:7]
#     women_products = Fragrance.objects.filter(category='Women').order_by('-id')[:7]
#     return render(request, 'homePage.html', {'men_products': men_products, 'women_products': women_products})

# def cart_item_count(request):
#     if request.user.is_authenticated:
#         cart_count = Cart.objects.filter(user=request.user).aggregate(total_count=Sum('quantity'))['total_count'] or 0
#     else:
#         cart_count = 0
#     return {'cart_item_count': cart_count}

# --------- #

# # views.py
# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import JsonResponse
# from .models import Fragrance, Cart
# from django.db.models import F
# from django.db.models.functions import Coalesce

# def homePage(request):
#     fragrance = Fragrance.objects.all()
#     sections = ['Men', 'Women']
#     return render(request, 'homePage.html', {'fragrance': fragrance, 'sections': sections})

# def productsByCategory(request, category):
#     filteredFragrances = Fragrance.objects.filter(category=category)

#     sort = request.GET.get('sort')
#     deals = request.GET.get('sale')
#     brand = request.GET.get('brand')

#     if sort == 'priceAsc':
#         filteredFragrances = filteredFragrances.annotate(effective_price=Coalesce('salePrice', 'price')).order_by('effective_price')
#     elif sort == 'priceDesc':
#         filteredFragrances = filteredFragrances.annotate(effective_price=Coalesce('salePrice', 'price')).order_by('-effective_price')

#     if deals == 'onSale':
#         filteredFragrances = filteredFragrances.filter(isOnSale=True)

#     if brand:
#         filteredFragrances = filteredFragrances.filter(brand=brand)

#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         data = {
#             'fragrance': [
#                 {
#                     'name': frag.name,
#                     'price': frag.price,
#                     'salePrice': frag.salePrice,
#                     'img': frag.img,
#                     'isOnSale': frag.isOnSale,
#                     'brand': frag.brand
#                 }
#                 for frag in filteredFragrances
#             ]
#         }
#         return JsonResponse(data)
#     return render(request, 'productsByCategory.html', {'fragrance': filteredFragrances, 'category': category})

# def order(request, id):
#     cart = request.session.get('cart', {})
#     strId = str(id)
#     product = Fragrance.objects.get(id=id)
#     quantity = int(request.POST.get('quantity', 1))
#     if strId in cart:
#         cart[strId]['quantity'] += quantity
#     else:
#         cart[strId] = {
#             'name': product.name,
#             'price': product.price,
#             'salePrice': product.salePrice,
#             'quantity': quantity,
#             'isOnSale': product.isOnSale,
#             'img': product.img,
#         }
#     request.session['cart'] = cart
#     return redirect('productsByCategory', category=product.category)

# def cart(request):
#     cart = request.session.get('cart', {})
#     total = 0
#     for item_id, item in cart.items():
#         salePrice = item['salePrice']
#         price = salePrice if salePrice else item['price']
#         item['total'] = price * item['quantity']
#         total += item['total']
#     return render(request, 'cart.html', {'cart': cart, 'total': total})

# def updateCart(request, id):
#     cart = request.session.get('cart', {})
#     strId = str(id)
#     if strId in cart:
#         newQuantity = int(request.POST.get('quantity', 1))
#         if newQuantity > 0:
#             cart[strId]['quantity'] = newQuantity
#         else:
#             del cart[strId]
#     request.session['cart'] = cart

#     return redirect('cart')

# def deleteFromCart(request, id):
#     cart = request.session.get('cart', {})
#     strId = str(id)
#     if strId in cart:
#         del cart[strId]
#     request.session['cart'] = cart
#     return redirect('cart')

# def thankyou(request):
#     return render(request, 'thankyou.html')

# def clearCart(request):
#     if request.method == 'POST':
#         request.session['cart'] = {}
#         return JsonResponse({'status': 'success', 'message': 'Cart cleared.'})
#     return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

# # Example of adding item to the cart
# def add_to_cart(request, fragrance_id):
#     if not request.user.is_authenticated:
#         return redirect('login')  # Redirect to login if not logged in

#     fragrance = get_object_or_404(Fragrance, id=fragrance_id)
#     cart_item, created = Cart.objects.get_or_create(user=request.user, fragrance=fragrance)
#     if not created:
#         cart_item.quantity += 1  # Increase quantity if the item is already in the cart
#     cart_item.save()
#     return redirect('cart')  # Redirect to the cart page

# def aboutPage(request):
#     return render(request, 'about.html')

