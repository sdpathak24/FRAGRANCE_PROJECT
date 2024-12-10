from  django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout, name='logout'),
    path('', views.homePage,  name='homePage'),
    path('about/', views.aboutPage, name='about'), 
    path('shop/<str:category>/', views.productsByCategory, name='productsByCategory'),
    path('order/<int:id>/', views.order, name='order'),
    path('cart/', views.cart, name='cart'),
    path('updateCart/<int:id>/', views.updateCart, name='updateCart'),
    path('deleteFromCart/<int:id>/', views.deleteFromCart, name='deleteFromCart'),
    path('thankyou/', views.thankyou, name='thankyou'),
    path('clearCart/', views.clearCart, name='clearCart')
]