# Realtime Chat App

اپلیکیشن چت گروهی بلادرنگ ساخته‌شده با Django و Django Channels.

## ویژگی‌ها

- ارتباط بلادرنگ با WebSocket از طریق `channels.generic.websocket.AsyncWebsocketConsumer`
- پیام‌رسانی گروهی با استفاده از Channel Layer (`group_add`, `group_send`)
- صفحه‌ی چت فقط برای کاربران احراز هویت‌شده در دسترسه (ریدایرکت به صفحه لاگین در غیر این صورت)
- ارسال و دریافت پیام به‌صورت JSON بین کلاینت و سرور

## تکنولوژی‌ها

- Django
- Django Channels (ASGI, WebSocket)

## راه‌اندازی محلی

```bash
git clone https://github.com/AminRst/realtime-chat-django.git
cd realtime-chat-django
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

> ⚠️ نیاز به `channels` و احتمالاً `channels-redis` برای production داره — این‌ها رو به `requirements.txt` اضافه کنید.

## نکاتی که بهتره قبل از نمایش اصلاح بشه

- [ ] اضافه کردن `requirements.txt`
- [ ] نام گروه چت (`group_chat_gfg`) هاردکد شده — بهتره بر اساس room id پویا باشه تا چند چت‌روم جدا پشتیبانی بشه
- [ ] اضافه کردن یک GIF یا اسکرین‌شات از چت در حال کار
