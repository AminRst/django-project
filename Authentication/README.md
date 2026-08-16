# Django Authentication System

پیاده‌سازی سیستم ثبت‌نام، ورود و مدیریت پروفایل کاربر با Django (بدون DRF، مبتنی بر Template).

## ویژگی‌ها

- ثبت‌نام با فرم سفارشی (`UserRegisterForm`) و همچنین نسخه‌ی ثبت‌نام با ایمیل
- ورود کاربر با `authenticate` + بررسی فعال بودن حساب (`is_active`)
- صفحه‌ی پروفایل کاربر
- اعتبارسنجی قدرت پسورد فعال است (حداقل طول، عدم شباهت به نام کاربری، رد پسوردهای رایج، غیرعددی بودن)
- پوشش تست: ثبت‌نام موفق، ثبت‌نام با پسورد نامطابق، ورود موفق، ورود با پسورد اشتباه

## تکنولوژی‌ها

- Django
- Django Forms & Auth

## راه‌اندازی محلی

```bash
git clone https://github.com/AminRst/django-project.git
cd django-project/Authentication
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# .env رو باز کن و SECRET_KEY رو تنظیم کن

python manage.py migrate
python manage.py runserver
```

اجرای تست‌ها:
```bash
python manage.py test accounts
```

## کارهایی که برای حرفه‌ای‌سازی این ریپو انجام شد

- **امنیت:** `SECRET_KEY` به متغیر محیطی منتقل شد (فایل نمونه `.env.example`).
- **تست:** `accounts/tests.py` که قبلاً کاملاً خالی بود، الان ۵ تست واقعی داره (ثبت‌نام، هش شدن پسورد، تطابق پسوردها، ورود موفق/ناموفق).
- `requirements.txt` اضافه شد.
