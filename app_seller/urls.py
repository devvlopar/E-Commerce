from django.urls import path
from app_seller import views
urlpatterns = [
    path('add-product/', views.add_product, name="add_product"),
    path('seller-register/', views.seller_register, name="seller_register"),
    path('seller-otp/', views.seller_otp, name="seller_otp"),
    path('seller-login/', views.seller_login, name="seller_login"),              
    path('seller-logout/', views.seller_logout, name="seller_logout"),
    path('delete/', views.delete, name="delete"),

    # path('seller-arrival/', views.seller_arrival, name="seller-arrival"),
]