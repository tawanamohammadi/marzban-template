# 🔍 بررسی دقیق: آیا روش پیشنهادی جواب می‌دهد؟

**تاریخ:** ۱۹ آذر ۱۴۰۳  
**سوال کاربر:** آیا لیست سرورها برای هر ساب فرق نمی‌کنه؟ باید از سرور دریافت بشه؟

---

## ✅ پاسخ: بله، کاملاً جواب می‌دهد!

### چرا؟

**Dashboard V4 Ultimate به صورت هوشمند طراحی شده:**

1. **از Marzban API لینک‌های واقعی می‌گیرد** (برای هر کاربر متفاوت)
2. **خودش لینک‌ها را پارس می‌کند** (در سمت Client)
3. **سرورها را دینامیک می‌سازد** (بدون نیاز به ارسال لیست جداگانه)

---

## 🔄 جریان کار واقعی

### مرحله 1: درخواست کاربر
```
کاربر → https://your-domain.com/sub/john_doe
```

### مرحله 2: Backend (FastAPI/Marzban)
```python
@app.get("/sub/{username}")
async def subscription_page(request: Request, username: str):
    # دریافت اطلاعات کاربر از Marzban API
    user = await get_user_from_marzban(username)
    
    # user شامل این فیلدهاست:
    # {
    #   "username": "john_doe",
    #   "status": {"value": "active"},
    #   "used_traffic": 1234567890,
    #   "data_limit": 50000000000,
    #   "expire": 1735123456,
    #   "online_at": 1735000000,
    #   "created_at": 1700000000,
    #   "links": [  # ⭐ این لیست برای هر کاربر متفاوت است
    #       "vless://uuid1@server1.com:443?...#US-Server",
    #       "vmess://base64...#DE-Server",
    #       "trojan://pass@server2.com:443#NL-Server"
    #   ]
    # }
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user  # ارسال به Template
    })
```

### مرحله 3: Template (Jinja2)
```html
<!-- dashboard.html -->
<script>
    // Jinja2 لیست لینک‌های این کاربر خاص را تزریق می‌کند
    const SUB_LINKS = [
        {% for link in user.links %}
        "{{ link }}",  // هر کاربر لینک‌های خودش را دارد
        {% endfor %}
    ];
    
    // مثال خروجی برای john_doe:
    // SUB_LINKS = [
    //     "vless://abc123@us1.example.com:443?...#US-Server-1",
    //     "vmess://xyz789...#DE-Server-2",
    //     "trojan://pass@nl1.example.com:443#NL-Server-3"
    // ];
    
    // مثال خروجی برای jane_smith (کاربر دیگر):
    // SUB_LINKS = [
    //     "vless://def456@fr1.example.com:443?...#FR-Server-1",
    //     "ss://base64...#GB-Server-2"
    // ];
</script>
```

### مرحله 4: JavaScript (Client-Side)
```javascript
// Dashboard V4 خودش لینک‌ها را پارس می‌کند
function parseLinks() {
    SERVERS = SUB_LINKS.map(link => {
        let name = "Server";
        let proto = "Unknown";
        let flag = "un";
        
        // پارس VLESS
        if (link.startsWith("vless://")) {
            proto = "VLESS";
            const parts = link.split("#");
            name = decodeURIComponent(parts[1] || "Server");
        }
        
        // پارس VMESS
        else if (link.startsWith("vmess://")) {
            proto = "VMESS";
            const json = JSON.parse(atob(link.substring(8)));
            name = json.ps || "Server";
        }
        
        // ... سایر پروتکل‌ها
        
        // تشخیص فلگ از نام
        const n = name.toLowerCase();
        if (n.includes("us")) flag = "us";
        else if (n.includes("de")) flag = "de";
        // ...
        
        return {
            flag: flag,
            name: name,
            proto: proto,
            link: link  // لینک اصلی نگه‌داری می‌شود
        };
    });
}

// نتیجه: هر کاربر لیست سرورهای خودش را می‌بیند!
```

---

## 📊 مقایسه: کاربر A vs کاربر B

### کاربر A (john_doe):
```
درخواست: /sub/john_doe

Marzban API Response:
{
    "username": "john_doe",
    "links": [
        "vless://...#US-Server-1",
        "vmess://...#DE-Server-2",
        "trojan://...#NL-Server-3"
    ]
}

Dashboard نمایش می‌دهد:
┌─────────────────┐
│ 🇺🇸 US Server 1 │
│ 🇩🇪 DE Server 2 │
│ 🇳🇱 NL Server 3 │
└─────────────────┘
```

### کاربر B (jane_smith):
```
درخواست: /sub/jane_smith

Marzban API Response:
{
    "username": "jane_smith",
    "links": [
        "vless://...#FR-Server-1",
        "ss://...#GB-Server-2",
        "trojan://...#TR-Server-3",
        "vmess://...#FI-Server-4"
    ]
}

Dashboard نمایش می‌دهد:
┌─────────────────┐
│ 🇫🇷 FR Server 1 │
│ 🇬🇧 GB Server 2 │
│ 🇹🇷 TR Server 3 │
│ 🇫🇮 FI Server 4 │
└─────────────────┘
```

---

## 🎯 اطلاعات مورد نیاز از Marzban API

### Endpoint اصلی:
```
GET /api/user/{username}
Authorization: Bearer {admin_token}
```

### Response مورد نیاز:
```json
{
    "username": "string",
    "status": "active" | "disabled" | "limited" | "expired",
    "used_traffic": 0,           // bytes
    "data_limit": 0,             // bytes
    "data_limit_reset_strategy": "no_reset",
    "expire": 0,                 // unix timestamp (null = unlimited)
    "online_at": 0,              // unix timestamp
    "created_at": 0,             // unix timestamp
    "links": [                   // ⭐ مهم‌ترین فیلد
        "vless://...",
        "vmess://...",
        "trojan://...",
        "ss://..."
    ],
    "subscription_url": "string",
    "proxies": {},
    "inbounds": {},
    "note": "string",
    "sub_updated_at": 0,
    "sub_last_user_agent": "string",
    "on_hold_expire_duration": 0,
    "on_hold_timeout": 0,
    "auto_delete_in_days": 0
}
```

### فیلدهای ضروری برای Dashboard V4:
```json
{
    "username": "john_doe",           // ✅ ضروری
    "status": "active",               // ✅ ضروری
    "used_traffic": 1234567890,       // ✅ ضروری
    "data_limit": 50000000000,        // ✅ ضروری
    "expire": 1735123456,             // ✅ ضروری
    "online_at": 1735000000,          // ✅ ضروری (برای "Last Seen")
    "created_at": 1700000000,         // ✅ ضروری (برای "Months With Us")
    "links": [                        // ✅ ضروری (برای لیست سرورها)
        "vless://...",
        "vmess://..."
    ]
}
```

---

## 🔧 کد نهایی صحیح برای Production

### فایل: `main.py`

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
import httpx
import uvicorn
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# تنظیمات Marzban
MARZBAN_URL = os.getenv("MARZBAN_URL", "https://your-marzban.com")
MARZBAN_TOKEN = os.getenv("MARZBAN_TOKEN", "your-admin-token")

async def get_user_from_marzban(username: str):
    """
    دریافت اطلاعات کاربر از Marzban API
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{MARZBAN_URL}/api/user/{username}",
                headers={"Authorization": f"Bearer {MARZBAN_TOKEN}"},
                timeout=10.0
            )
            
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="User not found")
            
            response.raise_for_status()
            user_data = response.json()
            
            # اطمینان از وجود فیلد status به صورت object
            if isinstance(user_data.get("status"), str):
                user_data["status"] = {"value": user_data["status"]}
            
            return user_data
            
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"Marzban API Error: {str(e)}")

@app.get("/sub/{username}")
async def subscription_page(request: Request, username: str):
    """
    نمایش Dashboard برای کاربر
    """
    # دریافت اطلاعات واقعی از Marzban
    user_data = await get_user_from_marzban(username)
    
    # ارسال به Template
    # Template خودش user.links را پارس می‌کند
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user_data  # شامل links برای این کاربر خاص
    })

@app.get("/manifest.json")
async def manifest():
    return FileResponse("manifest.json")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

---

## ✅ نتیجه‌گیری

### سوال: لیست سرورها برای هر ساب فرق می‌کنه؟
**پاسخ:** بله! و Dashboard V4 این را به درستی مدیریت می‌کند.

### چگونه؟
1. **Marzban API** برای هر کاربر `links` متفاوت برمی‌گرداند
2. **Backend (FastAPI)** این `links` را به Template ارسال می‌کند
3. **Template (Jinja2)** آن‌ها را به JavaScript تزریق می‌کند
4. **JavaScript (Client)** لینک‌ها را پارس کرده و UI می‌سازد

### آیا اطلاعات کافی داریم؟
**بله!** تنها چیزی که نیاز داریم:
- ✅ `username`
- ✅ `status`
- ✅ `used_traffic`
- ✅ `data_limit`
- ✅ `expire`
- ✅ `online_at`
- ✅ `created_at`
- ✅ `links` (مهم‌ترین فیلد)

همه این فیلدها در Response استاندارد Marzban API موجود هستند.

---

## 🎯 مراحل بعدی

1. **تست با Marzban واقعی:**
   ```bash
   # تنظیم متغیرهای محیطی
   export MARZBAN_URL="https://your-marzban.com"
   export MARZBAN_TOKEN="your-admin-token"
   
   # اجرا
   python main.py
   ```

2. **بررسی Response:**
   - آیا فیلد `links` وجود دارد؟
   - آیا فرمت لینک‌ها صحیح است؟

3. **تست با کاربران مختلف:**
   - `/sub/user1` → باید سرورهای user1 را نشان دهد
   - `/sub/user2` → باید سرورهای user2 را نشان دهد

---

**نتیجه:** روش پیشنهادی کاملاً صحیح است و برای هر کاربر، سرورهای مخصوص خودش را نمایش می‌دهد! 🎉
