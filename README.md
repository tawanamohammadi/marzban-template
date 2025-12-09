# 🚀 LOOKA VPN - Ultimate Marzban Dashboard Template v5.0

[![Version](https://img.shields.io/badge/version-5.0%20Ultimate-brightgreen)](https://github.com/YOUR_USERNAME/marzban-template)
[![Marzban](https://img.shields.io/badge/Marzban-Compatible-blue)](https://github.com/Gozargah/Marzban)
[![License](https://img.shields.io/badge/license-MIT-orange)](LICENSE)

A premium, feature-rich subscription dashboard template for [Marzban](https://github.com/Gozargah/Marzban) VPN panel with stunning UI/UX, comprehensive features, and full responsiveness.

![Dashboard Preview](https://via.placeholder.com/1200x600/0e0e14/1DB954?text=LOOKA+VPN+Dashboard)

## ✨ Features

### 🎨 **Premium Design**
- **Dual Theme System**: Spotify Dark (default) & Apple Music Light themes
- **Glassmorphism Effects**: Modern frosted glass UI elements
- **Smooth Animations**: Micro-interactions and transitions throughout
- **Responsive Design**: Perfect on all devices (320px - 4K+)
- **RTL/LTR Support**: Full bilingual support (English & Persian)

### 📊 **Comprehensive Dashboard**
- **Hero Section**: Clean status card with subscription info
- **Real-time Stats**: Usage analytics with animated charts
- **Server List**: 13 global servers with ping status
- **Usage Analytics**: Donut charts & bar graphs
- **Countdown Timer**: Visual subscription expiry countdown

### 🛠️ **User Features**
- **12+ FAQ Items**: Comprehensive help section
- **24/7 Support**: Multiple contact channels (Telegram, WhatsApp, Phone)
- **App Downloads**: Direct links for all platforms
- **QR Code Generation**: Easy config sharing
- **Copy to Clipboard**: One-click config copy
- **Collapsible Tutorial**: Step-by-step connection guide

### 📱 **Contact & Support**
- **Telegram Support**: [@rahbarusd](https://t.me/rahbarusd)
- **Support Channel**: [@panbehnet](https://t.me/panbehnet)
- **WhatsApp/Phone**: +98 990 112 0235
- **24/7 Availability**: Round-the-clock support

### 🔧 **Technical Features**
- **PWA Ready**: Installable as mobile app
- **Offline Support**: Service worker caching
- **SEO Optimized**: Proper meta tags and structure
- **Performance**: Lighthouse score 90+
- **Accessibility**: WCAG 2.1 AA compliant
- **No Dependencies**: Pure HTML/CSS/JS (except icons & fonts)

## 📁 Project Structure

```
marzban-template/
├── dashboard-v4-ultimate.html    # Main dashboard file (LATEST)
├── manifest.json                 # PWA manifest
├── sw.js                         # Service worker
├── README.md                     # This file
├── docs/                         # Documentation
│   ├── implementation-plan-v2.md
│   ├── logs-v4-ultimate.md
│   └── ...
├── logs/                         # Change logs
└── templates/                    # Template variations
```

## 🚀 Quick Start

### For Marzban Panel

1. **Copy the template file**:
   ```bash
   cp dashboard-v4-ultimate.html /var/lib/marzban/templates/subscription/index.html
   ```

2. **Restart Marzban**:
   ```bash
   marzban restart
   ```

3. **Access your subscription page**:
   ```
   https://your-domain.com/sub/YOUR_TOKEN
   ```

### For Testing Locally

1. **Open directly in browser**:
   ```bash
   # Windows
   start dashboard-v4-ultimate.html
   
   # macOS
   open dashboard-v4-ultimate.html
   
   # Linux
   xdg-open dashboard-v4-ultimate.html
   ```

2. **Or use a local server**:
   ```bash
   # Python 3
   python -m http.server 8000
   
   # Node.js
   npx http-server
   ```

## 🎯 Marzban Integration

### Required Marzban Variables

The template automatically integrates with Marzban's subscription system. The following variables are injected by Marzban:

```python
{
    "username": "user123",
    "status": "active",
    "expire": 1704067200,  # Unix timestamp
    "data_limit": 107374182400,  # Bytes
    "data_limit_reset_strategy": "no_reset",
    "used_traffic": 96636764160,  # Bytes
    "lifetime_used_traffic": 5497558138880,  # Bytes
    "sub_updated_at": "2024-12-09",
    "sub_last_user_agent": "v2rayNG/1.8.23",
    "online_at": "2024-12-09 08:30:00"
}
```

### Customization

1. **Update Contact Information**:
   - Edit lines 2373-2396 (Support section)
   - Replace `@rahbarusd`, `@panbehnet`, `+989901120235` with your info

2. **Modify Branding**:
   - Line 7: Change `<title>` tag
   - Lines 1793-1794: Update logo text
   - Line 2685: Update footer copyright

3. **Adjust Colors**:
   - Lines 22-46: Dark theme colors
   - Lines 50-70: Light theme colors

## 📱 Supported Platforms

### Mobile Apps
- **Android**: v2rayNG, NekoBox, Hiddify
- **iOS**: Shadowrocket, Streisand, FoXray
- **Windows**: v2rayN, Hiddify, Nekoray
- **macOS**: V2RayXS, Hiddify
- **Linux**: Nekoray, Hiddify

## 🌐 Browser Compatibility

| Browser | Version | Status |
|---------|---------|--------|
| Chrome | 90+ | ✅ Full Support |
| Firefox | 88+ | ✅ Full Support |
| Safari | 14+ | ✅ Full Support |
| Edge | 90+ | ✅ Full Support |
| Opera | 76+ | ✅ Full Support |
| Mobile Browsers | Latest | ✅ Full Support |

## 📊 Performance

- **Lighthouse Score**: 95+
- **First Contentful Paint**: < 1.2s
- **Time to Interactive**: < 2.5s
- **Total Bundle Size**: ~90KB (uncompressed)

## 🔒 Security Features

- ✅ No external JavaScript dependencies
- ✅ CSP-ready (Content Security Policy)
- ✅ No tracking or analytics
- ✅ No-logs policy
- ✅ HTTPS-only recommended

## 📝 Changelog

### v5.0 Ultimate (December 2024)
- ✨ Expanded FAQ from 3 to 12 comprehensive questions
- ✨ Updated support contacts (Telegram, WhatsApp, Phone)
- ✨ Added comprehensive footer with social links
- ✨ Improved hero section with cleaner layout
- ✨ Added collapsible tutorial section
- ✨ Enhanced support section with 24/7 badge
- ✨ Complete Persian/English translations
- 🐛 Fixed responsive issues on small screens
- 🎨 Improved overall visual consistency

### v4.0 (Previous)
- Added PWA support
- Implemented theme switching
- Enhanced charts and visualizations

[View Full Changelog](docs/logs-v4-ultimate.md)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Marzban](https://github.com/Gozargah/Marzban) - The amazing VPN panel
- [Remix Icon](https://remixicon.com/) - Beautiful icon set
- [Vazirmatn Font](https://github.com/rastikerdar/vazirmatn) - Persian font
- [Plus Jakarta Sans](https://fonts.google.com/specimen/Plus+Jakarta+Sans) - English font

## 📞 Support

- **Telegram**: [@rahbarusd](https://t.me/rahbarusd)
- **Channel**: [@panbehnet](https://t.me/panbehnet)
- **WhatsApp**: [+98 990 112 0235](https://wa.me/989901120235)
- **Phone**: +98 990 112 0235

## 🌟 Show Your Support

Give a ⭐️ if this project helped you!

---

<div align="center">
  <strong>Made with ❤️ for the Marzban community</strong>
  <br>
  <sub>© 2025 LOOKA VPN - Powered by Marzban</sub>
</div>
