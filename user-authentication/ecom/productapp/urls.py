from django.urls import path,include
from productapp import views
urlpatterns = [
    path('',views.product,name="product-home"),
]