# 🔄 V3.5 Restoration & Polish Plan

**Goal:** Restore missing features from V2 into V3 while maintaining the new interactive/interactive design language.

## 🏗️ Missing Features to Restore
1.  **Countdown Timer:**
    - Restore the `Days : Hours : Minnutes` countdown block.
    - Style it to match V3 cards (glassmorphism/clean).
2.  **Usage Analytics Bar Chart:**
    - Restore the "Daily Usage (Last 7 Days)" bar chart.
    - Integrate it into the V3 chart section or a new interactive modal.
3.  **Detailed Apps Section:**
    - Restore the full grid of apps with versions (v2rayNG, NekoBox, Hiddify, etc.) for all platforms.
    - Keep the V3 tabbed design but populate it with the rich data from V2.
4.  **Payment & Renewal:**
    - Restore the "Renew Subscription" card with Card Number, Holder, and Price Options.
    - Ensure it fits the Apple/Spotify theme.
5.  **Support Section:**
    - Restore Telegram/Email/Renew buttons.

## 🎨 Design Adaptation (V3 Style)
- **Cards:** Use `var(--card)` with `var(--r)` radius and `var(--border)`.
- **Interactivity:**
    - Apps: Click to download (direct) or show "How to install" modal.
    - Payment: Click price option to select.
- **Theme:** Ensure all new sections respect `data-theme="light"` and `dark`.

## 🛠️ Implementation Steps
1.  **Merge HTML:** Copy sections from V2 to V3.
2.  **Refactor CSS:** Update class names to match V3 (e.g., `pay-card` -> `card` style).
3.  **Update JS:** Bring back the logic for Tabs (Apps/Charts), Copy to Clipboard (Payment), and Time updates.
4.  **Verify:** Test all interactive elements and theme switching.

---
*Created by AI Assistant*
