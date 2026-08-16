# Realtime Chat App

اپلیکیشن چت گروهی بلادرنگ ساخته‌شده با Django و Django Channels.

## ویژگی‌ها

- ارتباط بلادرنگ با WebSocket از طریق `channels.generic.websocket.AsyncWebsocketConsumer`
- پشتیبانی از چند چت‌روم مستقل — نام روم بخشی از آدرس است (`/room/<room_name>/`)
- پیام‌رسانی گروهی با استفاده از Channel Layer (`group_add`, `group_send`)
- صفحه‌ی چت فقط برای کاربران احراز هویت‌شده در دسترسه (ریدایرکت به صفحه لاگین در غیر این صورت)
- ارسال و دریافت پیام به‌صورت JSON بین کلاینت و سرور

## تکنولوژی‌ها

- Django
- Django Channels + Daphne (ASGI)

## راه‌اندازی محلی

```bash
git clone https://github.com/AminRst/django-project.git
cd django-project/ChatApp
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# .env رو باز کن و SECRET_KEY رو تنظیم کن

python manage.py migrate
python manage.py runserver
```

بعد وارد `http://127.0.0.1:8000/room/general/` بشو (بعد از لاگین).

## کارهایی که برای حرفه‌ای‌سازی این ریپو انجام شد

- **باگ واقعی رفع شد:** توی `disconnect()`، آرگومان دوم `group_discard` اشتباه `self.channel_layer` (خودِ آبجکت لایه) بود به‌جای `self.channel_name` (شناسه‌ی کانکشن) — این باعث خطا موقع قطع اتصال هر کاربر می‌شد.
- **قابلیت جدید:** قبلاً فقط یک چت‌روم سراسری با نام هاردکد (`group_chat_gfg`) وجود داشت که همه‌ی کاربران سایت توش می‌افتادن؛ حالا هر روم یک آدرس مستقل داره و چندین چت‌روم مستقل می‌تونن هم‌زمان کار کنن.
- **امنیت:** `SECRET_KEY` به متغیر محیطی منتقل شد (فایل نمونه `.env.example`).
- `requirements.txt` اضافه شد.
