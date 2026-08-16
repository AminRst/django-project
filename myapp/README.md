# Cafe & Shop Platform (myapp)

پلتفرم چندبخشی به زبان فارسی برای معرفی و جست‌وجوی کافه‌ها، همراه با بلاگ و فروشگاه آنلاین — ساخته‌شده با Django.

## ویژگی‌ها

**دایرکتوری کافه (`business`)**
- ثبت و مدیریت کافه‌ها با آدرس، شهر (شیراز، نیویورک، منچستر)، وضعیت باز/بسته و منو
- جست‌وجوی متنی کافه‌ها با `TrigramSimilarity` (پستگرس)
- سیستم لایک، ذخیره (Save)، امتیازدهی (`django-star-ratings`) و کامنت روی هر کافه
- فرم تماس با ما و ثبت تیکت پشتیبانی
- کش کردن نتایج برای پرفورمنس بهتر

**بلاگ (`blog`)**
- پست‌های دسته‌بندی‌شده (نوشیدنی، فست‌فود، غذای سنتی و ...)
- سیستم پیش‌نویس/انتشار/رد پست، محاسبه خودکار زمان مطالعه
- کامنت و آپلود تصویر برای هر پست

**فروشگاه و سبد خرید (`shop`, `cart`)**
- دسته‌بندی و مدیریت محصول با موجودی، قیمت، تخفیف و ویژگی‌های سفارشی
- سبد خرید مبتنی بر session با محاسبه خودکار هزینه ارسال بر اساس وزن
- تاریخ شمسی برای ثبت محصولات (`django-jalali`)

## تکنولوژی‌ها

- **Backend:** Django, Django ORM
- **Database:** PostgreSQL (با پشتیبانی جستجوی Trigram)
- **بسته‌های کلیدی:** `django-jalali` (تاریخ شمسی), `django-resized` (تغییر سایز خودکار تصاویر), `django-star-ratings`, `jazzmin` (پنل ادمین سفارشی), `easy-thumbnails`
- **Frontend:** Bootstrap + فونت‌های فارسی سفارشی

## راه‌اندازی محلی

```bash
git clone https://github.com/AminRst/cafe-directory-platform.git
cd cafe-directory-platform
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

> ⚠️ فایل `requirements.txt` فعلاً در ریپو وجود نداره — پیشنهاد می‌کنم با `pip freeze > requirements.txt` بسازیدش تا نصب پروژه برای بقیه ساده بشه.

## نکاتی که قبل از نمایش به کارفرما بهتره اصلاح بشه

- [ ] اضافه کردن `requirements.txt`
- [ ] حذف `business/log/django.log` و `business/log/user.log` از ریپو (این‌ها فایل لاگ اجرا هستن، نباید کامیت بشن)
- [ ] جایگزینی کتابخانه‌های vendor شده (Bootstrap, jQuery, FontAwesome) با CDN یا `npm`/`pip` به‌جای کامیت مستقیم فایل‌ها
- [ ] حذف ویدیوهای بزرگ از پوشه `static/video`
- [ ] اضافه کردن چند اسکرین‌شات از رابط کاربری به این README
