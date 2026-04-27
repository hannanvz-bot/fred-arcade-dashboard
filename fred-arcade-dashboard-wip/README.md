# 🎮 FRED Arcade Dashboard

**Video Game Style Economic Data Explorer**

> *A work-in-progress project built during the "Algorithmic Trading & Market Modelling" workshop at MEF – Universidad de Navarra (UNAV).*

---

## 🚀 What is this?

FRED Arcade Dashboard is an interactive, **video-game-style** HTML dashboard that visualizes real economic indicators from the [Federal Reserve Economic Data (FRED)](https://fred.stlouisfed.org/) API. 

Instead of boring spreadsheets, you get:
- 🕹️ **Arcade cabinet UI** with retro pixel fonts
- 🎲 **Random indicator selector** (like a slot machine!)
- 📈 **Live Plotly charts** with recession shading
- ⚡ **Combo counter** with sound effects
- 📊 **Full metrics table** with color-coded changes
- ⏳ **Time warp buttons** (1Y, 3Y, 5Y, 10Y, ALL)
- 👻 **Recession toggle** overlay
- 🔊 **8-bit audio feedback** on every interaction

All data is **pre-loaded** into the HTML — no server, no CORS issues, no API calls from the browser. Just open the generated file and play!

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/fred-arcade-dashboard.git
cd fred-arcade-dashboard

# Install dependencies
pip install -r requirements.txt
```

### Requirements
- Python 3.8+
- `requests`
- `pandas`
- `numpy`

> Note: `plotly` is listed in `requirements.txt` for completeness, but it's only used via CDN in the generated HTML (no Python runtime dependency).

---

## 🎮 How to Use

1. **Run the Python script:**
   ```bash
   python fred_arcade_dashboard.py
   ```

2. **Wait for data fetching** (~10-20 seconds). The script downloads all FRED data and embeds it directly into the HTML.

3. **Open the generated file:**
   ```bash
   open fred_working_arcade.html   # macOS
   # or
   start fred_working_arcade.html  # Windows
   # or
   xdg-open fred_working_arcade.html  # Linux
   ```

4. **Press the big orange button** and explore economic data like it's 1985! 🕹️

---

## 📊 Included Indicators

| Indicator | FRED Code |
|-----------|-----------|
| Real GDP | `GDP` |
| Industrial Production | `INDPRO` |
| Unemployment Rate | `UNRATE` |
| CPI (All Urban) | `CPIAUCSL` |
| Fed Funds Rate | `FEDFUNDS` |
| 10-Year Treasury Yield | `DGS10` |
| M2 Money Stock | `M2SL` |
| S&P 500 Index | `SP500` |
| 10Y-2Y Treasury Spread | `T10Y2Y` |
| Baa Corporate Bond Yield | `BAA10Y` |

---

## 🚧 Work in Progress (WIP)

This is an **early-stage project** built in a single workshop session. Planned future features:

- [ ] 💾 **Save favorite indicators** to localStorage
- [ ] 🏆 **Leaderboard** for fastest "data exploration" combos
- [ ] 🎨 **More themes** (Cyberpunk, Terminal Green, Bloomberg Dark)
- [ ] 📤 **Export charts** as PNG/SVG
- [ ] 🔍 **Search & filter** the full FRED catalog (200,000+ series!)
- [ ] 📱 **Mobile-responsive** cabinet layout
- [ ] 🌐 **Live API mode** (optional, for real-time updates without re-running)
- [ ] 🤖 **ML-based anomaly detection** flash warnings

---

## ⚠️ API Key Notice

The FRED API key included in this repository is **for educational and demonstration purposes only**. 

For production use or heavy traffic, please obtain your own free API key at [https://fred.stlouisfed.org/docs/api/api_key.html](https://fred.stlouisfed.org/docs/api/api_key.html) and replace it in the script.

---

## 🙏 Credits

- **Data Source:** [Federal Reserve Economic Data (FRED)](https://fred.stlouisfed.org/) – Federal Reserve Bank of St. Louis
- **Course:** Algorithmic Trading & Market Modelling
- **Institution:** MEF – Universidad de Navarra (UNAV), Spain
- **Instructor:** Professor and workshop facilitator
- **Built with:** Python, Pandas, Plotly, and a lot of caffeine ☕

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) – free for educational and personal use.

---

> *"Economics is just a video game with real consequences."* 🎮📈
