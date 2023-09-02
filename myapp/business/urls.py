from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

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
    path('cafes/<cafe_id>/comment', views.cafe_comment, name='cafe_comment'),
    path('cafe/out_of_service/<int:id>', views.out_of_service, name='out_of_service'),
    path('city_cafes/', views.city_view, name='city_cafes'),
    path('search', views.cafe_search, name='cafe_search'),
    # path('images', views.image, name='images')
    path('auth/login/', LoginView.as_view(template_name='business/login_page1.html'), name='login-user'),
    path("auth/logout/", LogoutView.as_view(), name="logout-user")

]

