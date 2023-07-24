from django.urls import path
from . import views

app_name = 'business'
urlpatterns = [
    path('', views.index, name='index'),
    # path('cafe/', views.cafe_list, name='cafe_list'),
    path('cafes/', views.CafeListView.as_view(), name='cafe_list'),
    path('cafe/<int:id>', views.cafe_detail, name='cafe_detail'),
    # path('cafe/<pk>', views.CafeDetailView.as_view(), name='cafe_detail'),
    path('ticket/', views.ticket, name='ticket'),
    path('open_cafes/', views.OpenCafesListView.as_view(), name='open'),
    path('close_cafes/', views.CloseCafesListView.as_view(), name='close')

]