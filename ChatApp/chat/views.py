from django.shortcuts import render, redirect


def chat_page(request, room_name="general"):
    if not request.user.is_authenticated:
        return redirect("login-user")
    context = {"room_name": room_name}
    return render(request, "chat/chatPage.html", context)
