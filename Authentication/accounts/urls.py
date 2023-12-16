from django.urls import path
from django.contrib.auth import views as auth_view
from . import views

app_name = 'accounts'


urlpatterns = [
    path('', views.index, name='home'),
    path('register/', views.register, name='register'),
    # path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/", views.profile_view, name="profile"),
    path("login/", views.user_login, name="login"),
    path('email_register', views.email_register, name="email_register"),
    # path('login/', auth_view.LoginView.as_view(), name='login'),

]