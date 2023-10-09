from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views
from django.urls import re_path


app_name = 'business'
urlpatterns = [
    path('', views.index, name='index'),
    # path('cafe/', views.cafe_list, name='cafe_list'),
    path('cafes/', views.CafeListView.as_view(), name='cafe_list'),
    # path('cafes/<str:close_cafe>/', views.CafeListView.as_view(), name='cafe_close'),
    path('cafe/<int:id>', views.cafe_detail, name='cafe_detail'),
    # path('cafe/<pk>', views.CafeDetailView.as_view(), name='cafe_detail'),
    path('ticket/', views.ticket, name='ticket'),
    path('cafes/<str:status>', views.CafeListView.as_view(), name='cafe_status'),
    path('contact_us/', views.ContactUsView.as_view(), name='contact_us'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('cafes/<cafe_id>/', views.cafe_comment, name='cafe_comment'),
    path('cafe/out_of_service/<int:id>', views.out_of_service, name='out_of_service'),
    path('city_cafes/', views.city_view, name='city_cafes'),
    path('search/', views.cafe_search, name='cafe_search'),
    # path('images', views.image, name='images')
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('account/edit', views.edit_account, name='edit_account'),
    path('panel/', views.panel, name='panel'),
    path('profile/edit_cafe/<cafe_id>', views.edit_cafe, name='edit_cafe'),
    path('profile/create_cafe', views.create_cafe, name='create_cafe'),
    path('profile/delete_image/<image_id>', views.delete_image, name='delete_image'),
    path('like/', views.like, name='like'),
    path('menu/<cafe_id>', views.menu_items_view, name='menu')

]

