# گزارش بررسی و رفع مشکلات پروژه

**تاریخ:** ۱۹ آذر ۱۴۰۳  
**نسخه:** Audit Report v1.0  
**وضعیت:** 🔍 شناسایی کامل مشکلات

---

## 📋 خلاصه اجرایی

پروژه `marzban-template` دارای یک داشبورد پیشرفته V4 Ultimate است که به درستی به بک‌اند متصل نشده است. این گزارش تمام مشکلات شناسایی شده و راه‌حل‌های پیشنهادی را ارائه می‌دهد.

---

## 🔴 مشکلات شناسایی شده

### 1. عدم اتصال Frontend و Backend
**شدت:** بحرانی 🔴

**توضیح:**
- فایل `dashboard-v4-ultimate.html` (121KB، 3347 خط) به عنوان داشبورد اصلی ساخته شده اما استفاده نمی‌شود
- `main.py` در حال حاضر فایل قدیمی `templates/subscription.html` را سرو می‌کند
- داشبورد V4 دارای تمام قابلیت‌های پیشرفته است اما به دلیل عدم اتصال، غیرفعال است

**تأثیر:**
- کاربران داشبورد قدیمی و ساده را می‌بینند
- تمام ویژگی‌های V4 (تم‌های Spotify/Apple، انیمیشن‌ها، نمودارها) در دسترس نیست

---

### 2. ساختار داده Mock نادرست
**شدت:** متوسط 🟡

**توضیح:**
- `main.py` داده‌های ساده‌ای را ارسال می‌کند که با نیازهای V4 مطابقت ندارد
- V4 نیاز به فیلدهای اضافی دارد: `user.links`, `user.online_at`, `user.created_at`
- ساختار سرورها (`SERVERS`) در JavaScript داشبورد V4 از Jinja2 تغذیه می‌شود اما بک‌اند آن را ارسال نمی‌کند

**مثال مشکل:**
```python
# main.py - ساختار فعلی (ناقص)
{
    "username": username,
    "status": "active",
    "used_traffic": 1.57 * GB,
    "data_limit": 50.0 * GB,
    "expire": timestamp,
    "link": "https://..."
}

# V4 نیاز دارد:
{
    "username": username,
    "status": {"value": "active"},
    "used_traffic": 1.57 * GB,
    "data_limit": 50.0 * GB,
    "expire": timestamp,
    "online_at": timestamp,
    "created_at": timestamp,
    "links": ["vless://...", "vmess://..."]  # لیست کانفیگ‌ها
}
```

---

### 3. Service Worker نادرست
**شدت:** کم 🟢

**توضیح:**
- `sw.js` فایل `dashboard-v4-ultimate.html` را کش می‌کند
- این فایل یک HTML استاتیک است و نباید مستقیماً کش شود
- باید endpoint دینامیک (`/sub/{username}`) کش شود

**کد فعلی:**
```javascript
const ASSETS = [
    './dashboard-v4-ultimate.html',  // ❌ اشتباه
    './manifest.json',
    // ...
];
```

**کد صحیح:**
```javascript
const ASSETS = [
    './',  // ✅ صحیح - endpoint اصلی
    './manifest.json',
    // ...
];
```

---

### 4. مسیرهای Manifest نادرست
**شدت:** کم 🟢

**توضیح:**
- دو فایل `manifest.json` وجود دارد:
  - `manifest.json` (ریشه پروژه)
  - `templates/manifest.json`
- این باعث سردرگمی می‌شود و PWA به درستی کار نمی‌کند

---

## ✅ راه‌حل‌های پیشنهادی

### مرحله 1: انتقال Dashboard V4 به Templates
```bash
# جابجایی فایل اصلی
mv dashboard-v4-ultimate.html templates/dashboard.html
```

### مرحله 2: بروزرسانی Backend
**فایل:** `main.py`

```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
from datetime import datetime, timedelta

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_user_data(username: str):
    """داده‌های Mock با ساختار کامل Marzban"""
    now = datetime.now()
    return {
        "username": username,
        "status": {"value": "active"},
        "used_traffic": 1.57 * 1024 * 1024 * 1024,  # 1.57 GB
        "data_limit": 50.0 * 1024 * 1024 * 1024,    # 50 GB
        "expire": int((now + timedelta(days=30)).timestamp()),
        "online_at": int((now - timedelta(minutes=2)).timestamp()),
        "created_at": int((now - timedelta(days=300)).timestamp()),
        "links": [
            "vless://uuid@server1.com:443?security=tls#Server-US",
            "vmess://base64config#Server-DE",
            "trojan://password@server2.com:443#Server-NL"
        ]
    }

@app.get("/sub/{username}")
async def subscription_page(request: Request, username: str):
    user_data = get_user_data(username)
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user_data
    })

@app.get("/manifest.json")
async def manifest():
    return FileResponse("manifest.json")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

### مرحله 3: بروزرسانی Service Worker
**فایل:** `sw.js`

```javascript
const CACHE_NAME = 'marzban-v4-cache';
const ASSETS = [
    './',
    './manifest.json',
    'https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800;900&display=swap',
    'https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css',
    'https://cdn.jsdelivr.net/npm/flag-icons@7.2.3/css/flag-icons.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js'
];

self.addEventListener('install', (e) => {
    e.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
    );
    self.skipWaiting();
});

self.addEventListener('activate', (e) => {
    e.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(
                keys.filter(key => key !== CACHE_NAME)
                    .map(key => caches.delete(key))
            );
        })
    );
});

self.addEventListener('fetch', (e) => {
    e.respondWith(
        caches.match(e.request).then((response) => {
            return response || fetch(e.request);
        })
    );
});
```

### مرحله 4: حذف فایل‌های تکراری
```bash
# حذف manifest تکراری
rm templates/manifest.json

# آرشیو subscription.html قدیمی
mkdir -p docs/archive
mv templates/subscription.html docs/archive/
```

---

## 🧪 تست و راستی‌آزمایی

### تست محلی:
```bash
# 1. نصب وابستگی‌ها
pip install -r requirements.txt

# 2. اجرای سرور
python main.py

# 3. باز کردن مرورگر
# http://localhost:8000/sub/testuser
```

### چک‌لیست تست:
- [ ] داشبورد V4 نمایش داده می‌شود
- [ ] نام کاربری صحیح نمایش داده می‌شود
- [ ] داده‌های مصرف و انقضا صحیح است
- [ ] لیست سرورها نمایش داده می‌شود
- [ ] تغییر تم (Spotify/Apple) کار می‌کند
- [ ] تغییر زبان (EN/FA) کار می‌کند
- [ ] دکمه‌های کپی و QR کار می‌کنند
- [ ] PWA قابل نصب است

---

## 📊 اولویت‌بندی اقدامات

| اولویت | مشکل | زمان تخمینی | تأثیر |
|--------|------|-------------|-------|
| 🔴 P0 | اتصال V4 به Backend | 15 دقیقه | بحرانی |
| 🟡 P1 | تکمیل ساختار داده Mock | 10 دقیقه | زیاد |
| 🟢 P2 | رفع مشکل Service Worker | 5 دقیقه | متوسط |
| 🟢 P3 | پاکسازی فایل‌های تکراری | 2 دقیقه | کم |

**زمان کل تخمینی:** ~30 دقیقه

---

## 📝 یادداشت‌های مهم

1. **برای Production:**
   - داده‌های Mock را با API واقعی Marzban جایگزین کنید
   - از endpoint `/api/user/{username}` استفاده کنید
   - توکن احراز هویت را اضافه کنید

2. **امنیت:**
   - CORS را برای دامنه‌های مجاز تنظیم کنید
   - Rate limiting اضافه کنید
   - از HTTPS استفاده کنید

3. **بهینه‌سازی:**
   - فونت‌ها را محلی کنید (اختیاری)
   - تصاویر را بهینه کنید
   - از CDN برای فایل‌های استاتیک استفاده کنید

---

**گزارش تهیه شده توسط:** Antigravity AI  
**تاریخ:** ۱۹ آذر ۱۴۰۳
