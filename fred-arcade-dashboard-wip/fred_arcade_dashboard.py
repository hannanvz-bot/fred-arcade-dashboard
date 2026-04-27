"""
FRED Arcade Dashboard – Video Game Style Economic Data Explorer
===============================================================
A standalone HTML dashboard generator that embeds real FRED data
with an arcade/video game aesthetic.

Author: Student Project – MEF UNAV
Course: Algorithmic Trading & Market Modelling
Institution: MEF – Universidad de Navarra (UNAV)
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
import warnings
warnings.filterwarnings("ignore")

FRED_API_KEY = "ea8ac64394817916e385b32be98d0978"

PREDEFINED = {
    "Real GDP (GDP)": "GDP",
    "Industrial Production": "INDPRO",
    "Unemployment Rate": "UNRATE",
    "CPI (All Urban)": "CPIAUCSL",
    "Fed Funds Rate": "FEDFUNDS",
    "10-Year Treasury Yield": "DGS10",
    "M2 Money Stock": "M2SL",
    "S&P 500 Index": "SP500",
    "10Y-2Y Treasury Spread": "T10Y2Y",
    "Baa Corporate Bond Yield": "BAA10Y",
}

_cache = {}

def fetch_fred_series(series_id, start_date='2000-01-01', end_date=None):
    if end_date is None:
        end_date = datetime.today().strftime('%Y-%m-%d')
    cache_key = f"{series_id}_{start_date}_{end_date}"
    if cache_key in _cache:
        return _cache[cache_key].copy()

    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": start_date,
        "observation_end": end_date,
        "sort_order": "asc",
    }
    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        obs = data.get("observations", [])
        if not obs:
            return None
        df = pd.DataFrame(obs)
        df["date"] = pd.to_datetime(df["date"])
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        df = df[["date", "value"]].dropna()
        if df.empty:
            return None
        _cache[cache_key] = df
        return df.copy()
    except Exception as e:
        print(f"Error en {series_id}: {e}")
        return None

def get_recession_periods(start_date, end_date):
    df_rec = fetch_fred_series("USREC", start_date, end_date)
    if df_rec is None or df_rec.empty:
        return []
    in_rec = False
    periods = []
    start_rec = None
    for _, row in df_rec.iterrows():
        if row["value"] == 1 and not in_rec:
            in_rec = True
            start_rec = row["date"]
        elif row["value"] != 1 and in_rec:
            in_rec = False
            periods.append((start_rec.strftime('%Y-%m-%d'), row["date"].strftime('%Y-%m-%d')))
    if in_rec:
        periods.append((start_rec.strftime('%Y-%m-%d'), df_rec.iloc[-1]["date"].strftime('%Y-%m-%d')))
    return periods

def build_working_arcade():
    print("📡 Fetching all data from FRED (this will be embedded)...")
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = "2000-01-01"

    data_dict = {}
    for name, sid in PREDEFINED.items():
        df = fetch_fred_series(sid, start_date, end_date)
        if df is not None:
            data_dict[name] = df.set_index("date")["value"]

    if not data_dict:
        print("❌ No data. Check API key.")
        return

    df_all = pd.DataFrame(data_dict)
    df_all.dropna(how="all", inplace=True)
    recessions = get_recession_periods(start_date, end_date)

    series_data = {}
    metrics_all = []
    for col in df_all.columns:
        dates = df_all.index.strftime('%Y-%m-%d').tolist()
        values = df_all[col].fillna(method='ffill').tolist()
        latest_val = values[-1]
        latest_date = dates[-1]
        one_month_ago_idx = max(0, len(dates) - 30)
        val_1m = values[one_month_ago_idx]
        chg_1m = ((latest_val - val_1m) / val_1m * 100) if val_1m != 0 else None
        one_year_ago_idx = max(0, len(dates) - 365)
        val_1y = values[one_year_ago_idx]
        chg_1y = ((latest_val - val_1y) / val_1y * 100) if val_1y != 0 else None

        series_data[col] = {
            "dates": dates,
            "values": values,
            "latest": latest_val,
            "latest_date": latest_date,
            "chg_1m": chg_1m,
            "chg_1y": chg_1y
        }
        metrics_all.append({
            "name": col,
            "latest": latest_val,
            "chg_1m": chg_1m,
            "chg_1y": chg_1y
        })

    series_names = list(series_data.keys())

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>🎮 FRED ARCADE – WORKING DASHBOARD</title>
    <script src="https://cdn.plot.ly/plotly-2.24.1.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
        body {{
            background: linear-gradient(135deg, #0a0f1e, #0b1120);
            font-family: 'Press Start 2P', monospace;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .cabinet {{
            max-width: 1400px;
            width: 100%;
            background: #1a1f2e;
            border-radius: 32px;
            padding: 20px;
            border: 4px solid #ffd966;
            box-shadow: 0 0 0 3px #0f111a, 0 20px 40px black;
        }}
        .screen {{
            background: #0b0e14;
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 20px;
        }}
        h1 {{
            text-align: center;
            font-size: 1.4rem;
            color: #ffd966;
            text-shadow: 0 0 5px #ff9900;
            margin-bottom: 20px;
        }}
        .score-panel {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }}
        .card {{
            background: black;
            border: 2px solid #33ff33;
            border-radius: 12px;
            padding: 10px 15px;
            flex: 1;
            text-align: center;
        }}
        .card-label {{
            color: #33ff33;
            font-size: 0.6rem;
            margin-bottom: 8px;
        }}
        .card-value {{
            color: #ffd966;
            font-size: 0.9rem;
        }}
        #main-chart {{
            height: 450px;
            margin-top: 15px;
        }}
        .button-panel {{
            display: flex;
            gap: 15px;
            justify-content: center;
            margin: 20px 0;
            flex-wrap: wrap;
        }}
        .game-btn {{
            font-family: 'Press Start 2P', monospace;
            background: #2a2f3f;
            border: none;
            color: #ffd966;
            padding: 12px 20px;
            font-size: 0.7rem;
            cursor: pointer;
            box-shadow: 0 5px 0 #0f111a;
            border-radius: 12px;
            transition: 0.05s linear;
        }}
        .game-btn:active {{
            transform: translateY(3px);
            box-shadow: 0 2px 0 #0f111a;
        }}
        .btn-primary {{
            background: #e67e22;
            color: white;
            box-shadow: 0 5px 0 #b45f1b;
        }}
        .recession-btn {{
            background: #374151;
            color: #f87171;
        }}
        .time-bar {{
            display: flex;
            gap: 8px;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 10px;
        }}
        .time-btn {{
            font-family: 'Press Start 2P', monospace;
            background: #1f2937;
            border: 1px solid #4b5563;
            color: #9ca3af;
            padding: 6px 12px;
            font-size: 0.55rem;
            cursor: pointer;
            border-radius: 6px;
        }}
        .time-btn.active {{
            background: #ffd966;
            color: #1f2937;
        }}
        .metrics-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            font-size: 0.65rem;
        }}
        .metrics-table th, .metrics-table td {{
            border: 1px solid #2a2f3f;
            padding: 8px;
            text-align: left;
            color: #cbd5e1;
        }}
        .metrics-table th {{
            background: #0f172a;
            color: #ffd966;
        }}
        .footer {{
            text-align: center;
            margin-top: 20px;
            font-size: 0.5rem;
            color: #6b7280;
        }}
        .shake {{
            animation: shake 0.2s ease-in-out 0s 2;
        }}
        @keyframes shake {{
            0% {{ transform: translate(1px, 1px); }}
            50% {{ transform: translate(-1px, -1px); }}
            100% {{ transform: translate(0, 0); }}
        }}
    </style>
</head>
<body>
<div class="cabinet" id="cabinet">
    <div class="screen">
        <h1>🕹️ FRED ARCADE – REAL DATA, REAL ACTION 🕹️</h1>
        <div class="score-panel">
            <div class="card"><div class="card-label">🎯 CURRENT INDICATOR</div><div class="card-value" id="current-name">S&P 500 Index</div></div>
            <div class="card"><div class="card-label">📈 LATEST VALUE</div><div class="card-value" id="latest-val">—</div></div>
            <div class="card"><div class="card-label">📉 1M CHANGE %</div><div class="card-value" id="chg-1m">—</div></div>
            <div class="card"><div class="card-label">📅 1Y CHANGE %</div><div class="card-value" id="chg-1y">—</div></div>
            <div class="card"><div class="card-label">⚡ COMBO x</div><div class="card-value" id="combo-val">1</div></div>
        </div>
        <div id="main-chart"></div>
    </div>

    <div class="button-panel">
        <button class="game-btn btn-primary" id="play-btn">🔫 PRESS TO PLAY (RANDOM INDICATOR)</button>
        <button class="game-btn" id="random-compare">🎲 RANDOM COMPARE</button>
        <button class="game-btn recession-btn" id="recession-toggle">👻 RECESSION: ON</button>
        <button class="game-btn" id="reset-combo">🔄 RESET COMBO</button>
    </div>

    <div class="time-bar">
        <button class="time-btn" data-range="1Y">1Y</button>
        <button class="time-btn" data-range="3Y">3Y</button>
        <button class="time-btn" data-range="5Y">5Y</button>
        <button class="time-btn" data-range="10Y">10Y</button>
        <button class="time-btn active" data-range="all">ALL (2000+)</button>
    </div>

    <h3 style="color:#ffd966; font-size:0.8rem; margin-top:20px;">📋 FULL METRICS TABLE (all indicators)</h3>
    <table class="metrics-table" id="metrics-table">
        <thead><tr><th>Indicator</th><th>Latest Value</th><th>1M Change %</th><th>1Y Change %</th></tr></thead>
        <tbody id="metrics-body"></tbody>
    </table>
    <div class="footer">
        🎮 Every click picks a random indicator – updates chart, latest numbers, changes, and table highlight.
    </div>
</div>

<script>
    const seriesDB = {json.dumps(series_data)};
    const seriesNames = {json.dumps(series_names)};
    const recessionPeriods = {json.dumps(recessions)};
    const metricsData = {json.dumps(metrics_all)};

    let currentPrimary = "S&P 500 Index";
    let currentSecondary = null;
    let showRecession = true;
    let currentRange = "all";
    let combo = 1;
    let lastPlayTime = 0;
    let audioCtx = null;

    function beep(freq=660, duration=0.08) {{
        if (!audioCtx) {{
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        }}
        const now = audioCtx.currentTime;
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.frequency.value = freq;
        gain.gain.setValueAtTime(0.15, now);
        gain.gain.exponentialRampToValueAtTime(0.00001, now + duration);
        osc.start();
        osc.stop(now + duration);
    }}

    function shake() {{
        const el = document.getElementById('cabinet');
        el.classList.add('shake');
        setTimeout(() => el.classList.remove('shake'), 200);
    }}

    function updateCombo() {{
        const now = Date.now();
        if (now - lastPlayTime < 1200) {{
            combo = Math.min(combo + 1, 10);
        }} else {{
            combo = 1;
        }}
        lastPlayTime = now;
        document.getElementById('combo-val').innerText = combo;
        beep(440 + combo * 30, 0.07);
        shake();
    }}

    function plotChart() {{
        const primaryData = seriesDB[currentPrimary];
        if (!primaryData) return;
        let traces = [{{
            x: primaryData.dates,
            y: primaryData.values,
            name: currentPrimary,
            line: {{ color: '#ff9933', width: 2.5 }},
            hovertemplate: '%{{x}}<br>%{{y:.2f}}<extra></extra>'
        }}];
        if (currentSecondary && currentSecondary !== currentPrimary) {{
            const secData = seriesDB[currentSecondary];
            if (secData) {{
                traces.push({{
                    x: secData.dates,
                    y: secData.values,
                    name: currentSecondary,
                    line: {{ color: '#66ccff', width: 2, dash: 'dot' }},
                    hovertemplate: '%{{x}}<br>%{{y:.2f}}<extra></extra>'
                }});
            }}
        }}

        let shapes = [];
        if (showRecession) {{
            recessionPeriods.forEach(rec => {{
                shapes.push({{
                    type: 'rect', xref: 'x', yref: 'paper',
                    x0: rec[0], x1: rec[1], y0: 0, y1: 1,
                    fillcolor: '#ff3333', opacity: 0.15, layer: 'below', line: {{ width: 0 }}
                }});
            }});
        }}

        let xrange = null;
        if (currentRange !== 'all') {{
            const dates = primaryData.dates;
            const lastDate = new Date(dates[dates.length-1]);
            let startDate = new Date(lastDate);
            if (currentRange === '1Y') startDate.setFullYear(lastDate.getFullYear()-1);
            else if (currentRange === '3Y') startDate.setFullYear(lastDate.getFullYear()-3);
            else if (currentRange === '5Y') startDate.setFullYear(lastDate.getFullYear()-5);
            else if (currentRange === '10Y') startDate.setFullYear(lastDate.getFullYear()-10);
            xrange = [startDate.toISOString().split('T')[0], dates[dates.length-1]];
        }}

        const layout = {{
            title: {{
                text: currentSecondary ? `${{currentPrimary}} vs ${{currentSecondary}}` : currentPrimary,
                font: {{ family: 'Press Start 2P', size: 12, color: '#ffd966' }}
            }},
            xaxis: {{ title: 'Date', gridcolor: '#2a2f3f', color: '#cbd5e1', range: xrange }},
            yaxis: {{ title: 'Value', gridcolor: '#2a2f3f', color: '#cbd5e1' }},
            plot_bgcolor: '#0b0e14', paper_bgcolor: '#0b0e14',
            font: {{ color: '#e2e8f0' }}, hovermode: 'x unified',
            shapes: shapes,
            margin: {{ t: 60, l: 60, r: 30, b: 50 }}
        }};
        Plotly.newPlot('main-chart', traces, layout, {{ responsive: true }});
    }}

    function updateTopPanel() {{
        const data = seriesDB[currentPrimary];
        if (!data) return;
        document.getElementById('current-name').innerHTML = currentPrimary;
        document.getElementById('latest-val').innerHTML = data.latest.toFixed(2);
        const chg1m = data.chg_1m !== null ? data.chg_1m.toFixed(2) + '%' : 'N/A';
        const chg1y = data.chg_1y !== null ? data.chg_1y.toFixed(2) + '%' : 'N/A';
        document.getElementById('chg-1m').innerHTML = chg1m;
        document.getElementById('chg-1y').innerHTML = chg1y;
        if (data.chg_1m !== null) {{
            document.getElementById('chg-1m').style.color = data.chg_1m >= 0 ? '#4ade80' : '#f87171';
        }}
        if (data.chg_1y !== null) {{
            document.getElementById('chg-1y').style.color = data.chg_1y >= 0 ? '#4ade80' : '#f87171';
        }}
        const tbody = document.getElementById('metrics-body');
        tbody.innerHTML = metricsData.map(m => `
            <tr id="row-${{m.name.replace(/ /g, '_')}}" style="background: ${{m.name === currentPrimary ? '#2a3f5e' : 'transparent'}}">
                <td>${{m.name}}</td>
                <td>${{m.latest.toFixed(2)}}</td>
                <td style="color: ${{m.chg_1m >= 0 ? '#4ade80' : '#f87171'}}">${{m.chg_1m !== null ? m.chg_1m.toFixed(2)+'%' : 'N/A'}}</td>
                <td style="color: ${{m.chg_1y >= 0 ? '#4ade80' : '#f87171'}}">${{m.chg_1y !== null ? m.chg_1y.toFixed(2)+'%' : 'N/A'}}</td>
            </tr>
        `).join('');
    }}

    function randomPlay() {{
        let newName = currentPrimary;
        while (newName === currentPrimary && seriesNames.length > 1) {{
            newName = seriesNames[Math.floor(Math.random() * seriesNames.length)];
        }}
        currentPrimary = newName;
        currentSecondary = null;
        updateCombo();
        plotChart();
        updateTopPanel();
    }}

    function randomCompare() {{
        let candidates = seriesNames.filter(n => n !== currentPrimary);
        if (candidates.length === 0) return;
        let newSec = candidates[Math.floor(Math.random() * candidates.length)];
        currentSecondary = newSec;
        updateCombo();
        plotChart();
    }}

    function toggleRecession() {{
        showRecession = !showRecession;
        const btn = document.getElementById('recession-toggle');
        btn.innerHTML = showRecession ? "👻 RECESSION: ON" : "👻 RECESSION: OFF";
        plotChart();
        beep(300, 0.1);
    }}

    function resetCombo() {{
        combo = 1;
        document.getElementById('combo-val').innerText = combo;
        beep(880, 0.1);
    }}

    function setTimeRange(range) {{
        currentRange = range;
        plotChart();
        document.querySelectorAll('.time-btn').forEach(btn => {{
            btn.classList.remove('active');
            if (btn.getAttribute('data-range') === range) btn.classList.add('active');
        }});
    }}

    document.getElementById('play-btn').addEventListener('click', randomPlay);
    document.getElementById('random-compare').addEventListener('click', randomCompare);
    document.getElementById('recession-toggle').addEventListener('click', toggleRecession);
    document.getElementById('reset-combo').addEventListener('click', resetCombo);
    document.querySelectorAll('.time-btn').forEach(btn => {{
        btn.addEventListener('click', () => setTimeRange(btn.getAttribute('data-range')));
    }});

    updateTopPanel();
    plotChart();

    document.body.addEventListener('click', () => {{
        if (!audioCtx) {{
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            audioCtx.resume();
        }}
    }}, {{ once: true }});
</script>
</body>
</html>"""

    output_file = "fred_working_arcade.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ WORKING ARCADE DASHBOARD → {output_file}")
    print("🎮 Open it, press the big orange button, and watch numbers, charts, and table update instantly!")
    try:
        import webbrowser
        webbrowser.open(f"file://{os.path.abspath(output_file)}")
    except:
        pass

if __name__ == "__main__":
    build_working_arcade()
