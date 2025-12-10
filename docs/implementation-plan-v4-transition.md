# نقشه پیاده‌سازی: انتقال به Dashboard V4 Ultimate

**تاریخ:** ۱۹ آذر ۱۴۰۳  
**نسخه:** Implementation Plan v1.0  
**هدف:** اتصال Dashboard V4 Ultimate به Backend و رفع مشکلات

---

## 🎯 اهداف

1. ✅ فعال‌سازی Dashboard V4 Ultimate به عنوان رابط کاربری اصلی
2. ✅ اتصال صحیح Backend (FastAPI) به Frontend (Jinja2)
3. ✅ رفع مشکلات Service Worker و PWA
4. ✅ پاکسازی فایل‌های تکراری و قدیمی
5. ✅ آماده‌سازی برای اتصال به Marzban API

---

## 📋 پیش‌نیازها

### سوال مهم برای کاربر:
> **هدف نهایی این پروژه چیست؟**
> 
> - [ ] آپلود مستقیم به پنل Marzban (به عنوان Subscription Template)
> - [ ] اجرای مستقل به عنوان یک اپلیکیشن Python (FastAPI)
> - [ ] هر دو (توسعه محلی + آپلود به Marzban)
>
> **توضیح:** این تصمیم روی ساختار نهایی پروژه تأثیر می‌گذارد.

---

## 🔧 تغییرات پیشنهادی

### 1️⃣ سازماندهی فایل‌ها

#### قبل:
```
marzban-template/
├── dashboard-v4-ultimate.html    # ❌ در ریشه پروژه
├── manifest.json                 # ❌ تکراری
├── templates/
│   ├── subscription.html         # ❌ قدیمی
│   └── manifest.json             # ❌ تکراری
└── sw.js                         # ⚠️ مسیرهای اشتباه
```

#### بعد:
```
marzban-template/
├── manifest.json                 # ✅ یک نسخه
├── templates/
│   └── dashboard.html            # ✅ V4 Ultimate (تغییر نام)
├── sw.js                         # ✅ مسیرهای صحیح
└── docs/
    └── archive/
        └── subscription.html     # 📦 آرشیو
```

---

### 2️⃣ بروزرسانی Backend

**فایل:** `main.py`

#### تغییرات:

```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
import uvicorn
from datetime import datetime, timedelta

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_user_data(username: str):
    """
    ساختار داده Mock کامل برای Dashboard V4
    در Production این تابع باید با Marzban API جایگزین شود
    """
    now = datetime.now()
    
    # محاسبه تاریخ عضویت (10 ماه پیش)
    created_at = now - timedelta(days=300)
    
    # محاسبه آخرین اتصال (2 دقیقه پیش)
    online_at = now - timedelta(minutes=2)
    
    # تاریخ انقضا (30 روز بعد)
    expire = now + timedelta(days=30)
    
    return {
        "username": username,
        "status": {
            "value": "active"  # V4 انتظار object دارد، نه string
        },
        "used_traffic": int(1.57 * 1024 * 1024 * 1024),  # 1.57 GB
        "data_limit": int(50.0 * 1024 * 1024 * 1024),    # 50 GB
        "expire": int(expire.timestamp()),
        "online_at": int(online_at.timestamp()),
        "created_at": int(created_at.timestamp()),
        
        # لیست کانفیگ‌های سرور (V4 این را پارس می‌کند)
        "links": [
            "vless://a1b2c3d4-e5f6-7890-abcd-ef1234567890@us1.example.com:443?encryption=none&security=tls&sni=us1.example.com&type=tcp&headerType=none#🇺🇸 US Server 1",
            "vless://b2c3d4e5-f6a7-8901-bcde-f12345678901@de1.example.com:443?encryption=none&security=reality&sni=google.com&type=tcp&headerType=none#🇩🇪 DE Server 1",
            "vmess://eyJ2IjoiMiIsInBzIjoi8J+HqPCfh6YgQ0EgU2VydmVyIDEiLCJhZGQiOiJjYTEuZXhhbXBsZS5jb20iLCJwb3J0Ijo0NDMsImlkIjoiYzNkNGU1ZjYtYTdiOC05MDEyLWNkZWYtMTIzNDU2Nzg5MDEyIiwiYWlkIjowLCJuZXQiOiJ3cyIsInR5cGUiOiJub25lIiwiaG9zdCI6ImNhMS5leGFtcGxlLmNvbSIsInBhdGgiOiIvd3MiLCJ0bHMiOiJ0bHMifQ==",
            "trojan://d4e5f6a7-b8c9-0123-def1-234567890123@nl1.example.com:443?security=tls&sni=nl1.example.com&type=tcp#🇳🇱 NL Server 1",
            "vless://e5f6a7b8-c9d0-1234-ef12-345678901234@fr1.example.com:443?encryption=none&security=tls&sni=fr1.example.com&type=tcp#🇫🇷 FR Server 1",
            "vless://f6a7b8c9-d0e1-2345-f123-456789012345@gb1.example.com:443?encryption=none&security=reality&sni=microsoft.com&type=tcp#🇬🇧 GB Server 1",
            "vless://a7b8c9d0-e1f2-3456-1234-567890123456@tr1.example.com:443?encryption=none&security=tls&sni=tr1.example.com&type=tcp#🇹🇷 TR Server 1",
            "vmess://eyJ2IjoiMiIsInBzIjoi8J+HrPCfh6cgSVIgU2VydmVyIDEiLCJhZGQiOiJpcjEuZXhhbXBsZS5jb20iLCJwb3J0Ijo0NDMsImlkIjoiYjhjOWQwZTEtZjJhMy00NTY3LTEyMzQtNjc4OTAxMjM0NTY3IiwiYWlkIjowLCJuZXQiOiJ3cyIsInR5cGUiOiJub25lIiwiaG9zdCI6ImlyMS5leGFtcGxlLmNvbSIsInBhdGgiOiIvd3MiLCJ0bHMiOiJ0bHMifQ==",
            "trojan://c9d0e1f2-a3b4-5678-2345-789012345678@fi1.example.com:443?security=tls&sni=fi1.example.com&type=tcp#🇫🇮 FI Server 1",
            "vless://d0e1f2a3-b4c5-6789-3456-890123456789@pl1.example.com:443?encryption=none&security=tls&sni=pl1.example.com&type=tcp#🇵🇱 PL Server 1",
            "vless://e1f2a3b4-c5d6-7890-4567-901234567890@se1.example.com:443?encryption=none&security=reality&sni=cloudflare.com&type=tcp#🇸🇪 SE Server 1",
            "vless://f2a3b4c5-d6e7-8901-5678-012345678901@jp1.example.com:443?encryption=none&security=tls&sni=jp1.example.com&type=tcp#🇯🇵 JP Server 1",
            "trojan://a3b4c5d6-e7f8-9012-6789-123456789012@sg1.example.com:443?security=tls&sni=sg1.example.com&type=tcp#🇸🇬 SG Server 1"
        ]
    }

@app.get("/sub/{username}")
async def subscription_page(request: Request, username: str):
    """
    Endpoint اصلی برای نمایش Dashboard
    """
    user_data = get_user_data(username)
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user_data
    })

@app.get("/manifest.json")
async def manifest():
    """
    سرو فایل Manifest برای PWA
    """
    return FileResponse("manifest.json")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

---

### 3️⃣ بروزرسانی Service Worker

**فایل:** `sw.js`

```javascript
const CACHE_NAME = 'marzban-v4-cache';
const ASSETS = [
    './',  // ✅ Endpoint اصلی (نه فایل HTML)
    './manifest.json',
    'https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800;900&display=swap',
    'https://cdn.jsdelivr.net/gh/niclis/vazir-font@v30.1.0/dist/Vazirmatn-Variable.css',
    'https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css',
    'https://cdn.jsdelivr.net/npm/flag-icons@7.2.3/css/flag-icons.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js'
];

self.addEventListener('install', (e) => {
    console.log('[SW] Installing...');
    e.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('[SW] Caching assets');
            return cache.addAll(ASSETS);
        })
    );
    self.skipWaiting();
});

self.addEventListener('activate', (e) => {
    console.log('[SW] Activating...');
    e.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(
                keys.filter(key => key !== CACHE_NAME)
                    .map(key => {
                        console.log('[SW] Deleting old cache:', key);
                        return caches.delete(key);
                    })
            );
        })
    );
    return self.clients.claim();
});

self.addEventListener('fetch', (e) => {
    e.respondWith(
        caches.match(e.request).then((response) => {
            if (response) {
                console.log('[SW] Serving from cache:', e.request.url);
                return response;
            }
            console.log('[SW] Fetching:', e.request.url);
            return fetch(e.request);
        })
    );
});
```

---

### 4️⃣ بروزرسانی Manifest

**فایل:** `manifest.json` (ریشه پروژه)

```json
{
    "name": "LOOKA VPN Dashboard",
    "short_name": "LOOKA",
    "description": "Premium VPN Subscription Dashboard",
    "start_url": "./",
    "display": "standalone",
    "background_color": "#020204",
    "theme_color": "#1DB954",
    "orientation": "portrait-primary",
    "icons": [
        {
            "src": "https://api.dicebear.com/7.x/shapes/svg?seed=LOOKA&backgroundColor=1DB954",
            "sizes": "192x192",
            "type": "image/svg+xml",
            "purpose": "any maskable"
        },
        {
            "src": "https://api.dicebear.com/7.x/shapes/svg?seed=LOOKA&backgroundColor=1DB954",
            "sizes": "512x512",
            "type": "image/svg+xml",
            "purpose": "any maskable"
        }
    ]
}
```

---

## 🚀 مراحل اجرا

### مرحله 1: Backup
```bash
# ایجاد نسخه پشتیبان
mkdir -p backups
cp -r templates backups/templates_$(date +%Y%m%d)
cp main.py backups/main_$(date +%Y%m%d).py
cp sw.js backups/sw_$(date +%Y%m%d).js
```

### مرحله 2: جابجایی فایل‌ها
```bash
# انتقال V4 به templates
mv dashboard-v4-ultimate.html templates/dashboard.html

# آرشیو فایل قدیمی
mkdir -p docs/archive
mv templates/subscription.html docs/archive/

# حذف manifest تکراری
rm templates/manifest.json
```

### مرحله 3: بروزرسانی کدها
```bash
# بروزرسانی main.py (کد بالا را کپی کنید)
# بروزرسانی sw.js (کد بالا را کپی کنید)
# بروزرسانی manifest.json (کد بالا را کپی کنید)
```

### مرحله 4: تست
```bash
# نصب وابستگی‌ها
pip install -r requirements.txt

# اجرای سرور
python main.py

# باز کردن مرورگر
# http://localhost:8000/sub/testuser
```

---

## ✅ چک‌لیست تست

### تست‌های بصری:
- [ ] داشبورد V4 Ultimate نمایش داده می‌شود
- [ ] تم Spotify Dark (پیش‌فرض) فعال است
- [ ] تغییر به تم Apple Music Light کار می‌کند
- [ ] آواتار کاربر (Dicebear) نمایش داده می‌شود
- [ ] نام کاربری صحیح است (`testuser`)

### تست‌های داده:
- [ ] روزهای باقیمانده: `30` نمایش داده می‌شود
- [ ] حجم مصرفی: `1.57 GB` نمایش داده می‌شود
- [ ] حجم کل: `50 GB` نمایش داده می‌شود
- [ ] درصد مصرف: `~3%` نمایش داده می‌شود
- [ ] ماه‌های عضویت: `10` نمایش داده می‌شود
- [ ] تعداد سرورها: `13` نمایش داده می‌شود

### تست‌های تعاملی:
- [ ] دکمه "Copy All" کار می‌کند
- [ ] دکمه "QR Code" کار می‌کند
- [ ] دکمه "Renew" کار می‌کند
- [ ] کلیک روی هر سرور Modal باز می‌شود
- [ ] تغییر زبان (EN/FA) کار می‌کند
- [ ] Tutorial قابل باز/بسته شدن است

### تست‌های PWA:
- [ ] دکمه "Install App" در مرورگر نمایش داده می‌شود
- [ ] نصب PWA موفقیت‌آمیز است
- [ ] آیکون و نام صحیح است
- [ ] حالت Standalone کار می‌کند

---

## 🔮 مراحل بعدی (اختیاری)

### برای Production:
1. **اتصال به Marzban API:**
   ```python
   import httpx
   
   async def get_user_from_marzban(username: str):
       async with httpx.AsyncClient() as client:
           response = await client.get(
               f"https://your-marzban.com/api/user/{username}",
               headers={"Authorization": f"Bearer {MARZBAN_TOKEN}"}
           )
           return response.json()
   ```

2. **افزودن Authentication:**
   - استفاده از JWT Token
   - محدودیت دسترسی به صفحه

3. **بهینه‌سازی:**
   - Minify کردن HTML/CSS/JS
   - استفاده از CDN
   - فعال‌سازی Gzip

---

## 📊 زمان‌بندی تخمینی

| مرحله | زمان | توضیح |
|--------|------|-------|
| Backup | 2 دقیقه | کپی فایل‌ها |
| جابجایی | 3 دقیقه | انتقال و حذف |
| بروزرسانی کد | 15 دقیقه | ویرایش main.py, sw.js |
| تست | 10 دقیقه | بررسی تمام قابلیت‌ها |
| **جمع** | **30 دقیقه** | |

---

## ⚠️ نکات مهم

1. **قبل از شروع:**
   - حتماً Backup بگیرید
   - Git commit کنید (اگر از Git استفاده می‌کنید)

2. **در حین کار:**
   - هر مرحله را جداگانه تست کنید
   - Console مرورگر را چک کنید (F12)
   - Network tab را برای بررسی درخواست‌ها ببینید

3. **بعد از اتمام:**
   - تمام چک‌لیست‌ها را تست کنید
   - روی دستگاه‌های مختلف امتحان کنید (موبایل/دسکتاپ)

---

**نقشه تهیه شده توسط:** Antigravity AI  
**تاریخ:** ۱۹ آذر ۱۴۰۳  
**وضعیت:** ✅ آماده اجرا
