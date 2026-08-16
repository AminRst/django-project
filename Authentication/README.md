# Django Authentication System

پیاده‌سازی سیستم ثبت‌نام، ورود و مدیریت پروفایل کاربر با Django (بدون DRF، مبتنی بر Template).

## ویژگی‌ها

- ثبت‌نام با فرم سفارشی (`UserRegisterForm`) و همچنین نسخه‌ی ثبت‌نام با ایمیل
- ورود کاربر با `authenticate` + بررسی فعال بودن حساب (`is_active`)
- صفحه‌ی پروفایل کاربر
- استفاده از فرم‌های استاندارد Django به‌جای پیاده‌سازی دستی احراز هویت

## تکنولوژی‌ها

- Django
- Django Forms & Auth

## راه‌اندازی محلی

```bash
git clone https://github.com/AminRst/django-auth-system.git
cd django-auth-system
python -m venv venv && source venv/bin/activate
pip install django
python manage.py migrate
python manage.py runserver
```

## نکاتی که بهتره قبل از نمایش اصلاح بشه

- [ ] اضافه کردن `requirements.txt`
- [ ] رمز عبور با `set_password` هش می‌شه که خوبه، ولی اعتبارسنجی قدرت پسورد (`AUTH_PASSWORD_VALIDATORS`) رو هم فعال/بررسی کنید
- [ ] اضافه کردن تست‌های واقعی در `tests.py` (فایل فعلی خالیه)
