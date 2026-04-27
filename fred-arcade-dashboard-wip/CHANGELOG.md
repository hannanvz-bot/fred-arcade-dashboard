# Changelog

All notable changes to the FRED Arcade Dashboard project will be documented in this file.

## [0.1.0] – 2026-04-27 – 🎮 Initial Arcade Release

### Added
- 🎮 Arcade cabinet UI with retro pixel font (`Press Start 2P`)
- 📡 FRED API integration with 10 predefined economic indicators
- 🎲 Random indicator selector with combo counter
- 📈 Interactive Plotly charts with hover tooltips
- 👻 Recession period overlay toggle (shaded red zones)
- ⏳ Time range buttons: 1Y, 3Y, 5Y, 10Y, ALL (2000+)
- 📊 Full metrics table with color-coded 1M / 1Y changes
- 🔊 8-bit sound effects via Web Audio API
- 💾 Standalone HTML generation — no server required
- 🎲 Random compare mode (dual-indicator overlay)
- 📱 Responsive layout (desktop optimized)

### Technical
- Python 3.8+ script with `requests`, `pandas`, `numpy`
- Embedded JSON data (no CORS, no live API calls from browser)
- In-memory caching for FRED API requests
- Recession data fetched from `USREC` series

### Known Issues / WIP
- Mobile layout needs refinement
- Only 10 indicators pre-loaded (FRED has 200,000+)
- No persistent user preferences (localStorage planned)
- API key hardcoded (educational use only)
- No export functionality for charts

## [Unreleased] – Future Ideas

### Planned
- [ ] 💾 Save favorite indicators to localStorage
- [ ] 🏆 Combo leaderboard / achievement system
- [ ] 🎨 Multiple visual themes (Cyberpunk, Terminal, Bloomberg)
- [ ] 📤 Export charts as PNG/SVG
- [ ] 🔍 Full FRED catalog search & filter
- [ ] 📱 True mobile-responsive cabinet
- [ ] 🌐 Optional live API mode for real-time updates
- [ ] 🤖 ML anomaly detection alerts
- [ ] 🌍 Multi-country economic data support
- [ ] 🎵 More sound effects and background music

---

> **Note:** This is a student workshop project. Versions follow [SemVer](https://semver.org/).
