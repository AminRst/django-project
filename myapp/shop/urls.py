from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('products', views.product_list, name='products'),
    path('products/<slug:category_slug>', views.product_list, name='product_list_by_category'),
    path('products/<int:id>/<slug:slug>', views.product_details, name='product_detail')
]
