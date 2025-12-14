# 🚀 Marzban V4 Ultimate Dashboard

[![Version](https://img.shields.io/badge/version-4.0%20Ultimate-brightgreen)](https://github.com/tawanamohammadi/marzban-template)
[![Marzban](https://img.shields.io/badge/Marzban-Compatible-blue)](https://github.com/Gozargah/Marzban)
[![License](https://img.shields.io/badge/license-Proprietary-red)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue)](https://www.python.org/)

A premium, feature-rich subscription dashboard for [Marzban](https://github.com/Gozargah/Marzban) VPN panel with stunning UI/UX, FastAPI backend, and full Marzban API integration.

![Dashboard Preview](https://via.placeholder.com/1200x600/0e0e14/1DB954?text=Marzban+V4+Dashboard)

## ✨ Features

### 🎨 **Premium Design**
- **Dual Theme System**: Spotify Dark (default) & Apple Music Light themes
- **Glassmorphism Effects**: Modern frosted glass UI elements
- **Smooth Animations**: Micro-interactions and transitions throughout
- **Responsive Design**: Perfect on all devices (320px - 4K+)
- **RTL/LTR Support**: Full bilingual support (English & Persian)

### 📊 **Comprehensive Dashboard**
- **Dynamic Server List**: Automatically parses user's subscription links
- **Real-time Stats**: Usage analytics with animated charts
- **Countdown Timer**: Visual subscription expiry countdown
- **Usage Analytics**: Donut charts & bar graphs
- **Server Details**: Click any server for QR code and details

### 🛠️ **Backend Features**
- **FastAPI Backend**: Modern async Python framework
- **Marzban API Integration**: Direct connection to Marzban panel
- **Development Mode**: Mock data for local testing
- **Production Mode**: Live data from Marzban API
- **Auto Data Normalization**: Ensures compatibility with V4 dashboard

### 📱 **User Features**
- **12+ FAQ Items**: Comprehensive help section
- **24/7 Support**: Multiple contact channels
- **QR Code Generation**: Easy config sharing
- **Copy to Clipboard**: One-click config copy
- **Collapsible Tutorial**: Step-by-step connection guide
- **PWA Ready**: Installable as mobile app

## 📁 Project Structure

```
marzban-template/
├── main.py                      # FastAPI backend (NEW)
├── requirements.txt             # Python dependencies (NEW)
├── manifest.json                # PWA manifest
├── sw.js                        # Service worker
├── templates/
│   └── dashboard.html           # V4 Ultimate Dashboard (Jinja2)
├── docs/
│   ├── project-audit-report.md
│   ├── implementation-plan-v4-transition.md
│   ├── technical-verification.md
│   └── archive/                 # Old files
└── README.md                    # This file
```

## 🚀 Quick Start

### Method 1: Direct Installation on Marzban Server (Recommended)

**This is the simplest and recommended method for production use.**

#### Step 1: SSH to your Marzban server
```bash
ssh user@your-server.com
```

#### Step 2: Create templates directory
```bash
mkdir -p /var/lib/marzban/templates/subscription
```

#### Step 3: Download the dashboard file
```bash
wget -O /var/lib/marzban/templates/subscription/index.html \
  https://raw.githubusercontent.com/tawanamohammadi/marzban-template/main/templates/dashboard.html
```

#### Step 4: Restart Marzban
```bash
marzban restart
```

#### Step 5: Access your subscription page
```
https://your-domain.com/sub/{username}
```

**That's it!** Marzban will automatically inject user data into the dashboard.

**Advantages:**
- ✅ No additional setup required
- ✅ No need for Python or dependencies
- ✅ No need for API tokens
- ✅ Marzban handles everything automatically
- ✅ Works out of the box

---

### Method 2: Local Development/Testing (Optional)

**Only use this if you want to test locally or develop custom features.**

#### Step 1: Clone the repository
```bash
git clone https://github.com/tawanamohammadi/marzban-template.git
```

#### Step 2: Enter the directory
```bash
cd marzban-template
```

#### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Run the development server
```bash
python main.py
```

#### Step 5: Open in browser
```
http://localhost:8000/sub/testuser
```

The server will use mock data automatically (13 sample servers, realistic stats).

---

### Method 3: Standalone Production Server (Advanced)

**Only use this if you want to run the dashboard as a separate service from Marzban.**

#### Step 1: Clone the repository
```bash
git clone https://github.com/tawanamohammadi/marzban-template.git
```

#### Step 2: Enter the directory
```bash
cd marzban-template
```

#### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Set environment variables

**Windows PowerShell:**
```powershell
$env:MARZBAN_URL="https://your-marzban.com"
$env:MARZBAN_TOKEN="your-admin-token-here"
```

**Linux/Mac:**
```bash
export MARZBAN_URL="https://your-marzban.com"
export MARZBAN_TOKEN="your-admin-token-here"
```

#### Step 5: Run the production server
```bash
python main.py
```

#### Step 4: Access dashboard
```
http://localhost:8000/sub/{username}
```

> **Note**: For most users, **Method 1 (Direct Installation)** is the best choice!

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `MARZBAN_URL` | Your Marzban panel URL | Production | `http://localhost:8080` |
| `MARZBAN_TOKEN` | Admin API token from Marzban | Production | `""` (Dev Mode) |

### Getting Marzban API Token

1. Login to your Marzban panel
2. Go to **Settings** → **API**
3. Create a new admin token
4. Copy the token and use it in `MARZBAN_TOKEN`

## 📊 How It Works

### Data Flow

```
User Request → FastAPI Backend → Marzban API → User Data
                     ↓
              Jinja2 Template → Dashboard HTML
                     ↓
              JavaScript Parser → Server List
                     ↓
              Rendered Dashboard
```

### Server List Generation

The dashboard **automatically parses** the user's subscription links:

1. Backend fetches `user.links` from Marzban API
2. Jinja2 injects links into JavaScript
3. Client-side parser extracts:
   - Server name
   - Protocol (VLESS, VMESS, Trojan, SS)
   - Country flag (from server name)
   - Connection type (TLS, Reality, WS)

**Result**: Each user sees their own unique server list!

## 🎯 Marzban API Integration

### Required User Data

The dashboard expects the following fields from Marzban API:

```python
{
    "username": "john_doe",
    "status": "active",              # or {"value": "active"}
    "used_traffic": 1234567890,      # bytes
    "data_limit": 50000000000,       # bytes
    "expire": 1735123456,            # unix timestamp
    "online_at": 1735000000,         # unix timestamp (for "Last Seen")
    "created_at": 1700000000,        # unix timestamp (for "Months With Us")
    "links": [                       # List of subscription links
        "vless://...",
        "vmess://...",
        "trojan://..."
    ]
}
```

All fields are provided by Marzban's standard `/api/user/{username}` endpoint.

## 🛠️ Customization

### 1. Update Contact Information

Edit `templates/dashboard.html`:

- **Support Section** (lines ~2550-2577): Update Telegram, WhatsApp, Phone
- **Footer** (lines ~2680-2740): Update social links and copyright

### 2. Modify Branding

- **Logo** (line ~2197): Change `LOOKA` text
- **Title** (line 7): Update page title
- **Footer** (line ~2730): Update copyright text

### 3. Adjust Colors

Edit CSS variables in `templates/dashboard.html`:

```css
/* Dark Theme (lines 20-47) */
:root[data-theme="dark"] {
    --accent: #1DB954;  /* Primary color */
    --bg: #020204;      /* Background */
    /* ... */
}

/* Light Theme (lines 50-70) */
:root[data-theme="light"] {
    --accent: #fa2d48;  /* Primary color */
    --bg: #f5f5f7;      /* Background */
    /* ... */
}
```

## 📱 Supported Platforms

### Client Apps
- **Android**: v2rayNG, NekoBox, Hiddify
- **iOS**: Shadowrocket, Streisand, FoXray
- **Windows**: v2rayN, Hiddify, Nekoray
- **macOS**: V2RayXS, Hiddify
- **Linux**: Nekoray, Hiddify

### Browsers
| Browser | Version | Status |
|---------|---------|--------|
| Chrome | 90+ | ✅ Full Support |
| Firefox | 88+ | ✅ Full Support |
| Safari | 14+ | ✅ Full Support |
| Edge | 90+ | ✅ Full Support |

## 🔒 Security

- ✅ No external JavaScript dependencies (except CDN fonts/icons)
- ✅ HTTPS recommended for production
- ✅ No tracking or analytics
- ✅ Environment variables for sensitive data
- ✅ CORS-ready for API integration

## 📝 Changelog

### v4.0 Ultimate (December 2024)
- ✨ **NEW**: FastAPI backend with Marzban API integration
- ✨ **NEW**: Development mode with mock data
- ✨ **NEW**: Production mode with live Marzban data
- ✨ **NEW**: Dynamic server list from user's subscription links
- ✨ **NEW**: Automatic data normalization
- ✨ Improved service worker caching
- ✨ Complete Persian/English translations
- ✨ Enhanced PWA support
- 🐛 Fixed responsive issues
- 📚 Comprehensive documentation

[View Full Documentation](docs/)

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository at [github.com/tawanamohammadi/marzban-template](https://github.com/tawanamohammadi/marzban-template)
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Marzban](https://github.com/Gozargah/Marzban) - The amazing VPN panel
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Remix Icon](https://remixicon.com/) - Beautiful icon set
- [Vazirmatn Font](https://github.com/rastikerdar/vazirmatn) - Persian font
- [Plus Jakarta Sans](https://fonts.google.com/specimen/Plus+Jakarta+Sans) - English font

## 📞 Support

- **Telegram**: [@rahbarusd](https://t.me/rahbarusd)
- **Channel**: [@panbehnet](https://t.me/panbehnet)
- **WhatsApp**: [+98 990 112 0235](https://wa.me/989901120235)

## 🌟 Show Your Support

Give a ⭐️ if this project helped you!

---

<div align="center">
  <strong>Made with ❤️ for the Marzban community</strong>
  <br>
  <sub>© 2025 Marzban V4 Dashboard - Powered by FastAPI & Marzban</sub>
</div>
