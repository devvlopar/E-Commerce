from django.urls import path
from app_buyer import views
urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register, name="register"),
    path('otp/', views.otp, name="otp"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('cart/', views.cart, name="cart"),

    path('arrival/', views.arrival, name="arrival"),
    path('add_to_cart/<int:pk>', views.add_to_cart, name="add_to_cart"),

    path('buyer_profile/', views.buyer_profile, name="buyer_profile"),

]