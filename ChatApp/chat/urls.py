from django.urls import path
from chat import views as chat_views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", chat_views.chat_page, name="chat-page"),
    path("room/<str:room_name>/", chat_views.chat_page, name="chat-room"),

    # login-section
    path("auth/login/", LoginView.as_view(template_name="chat/LoginPage.html"), name="login-user"),
    path("auth/logout/", LogoutView.as_view(), name="logout-user"),
]
