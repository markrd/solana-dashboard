import os
# (Not required on Streamlit Cloud, but harmless)
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"

import requests
import streamlit as st
from datetime import datetime, timezone, timedelta

st.set_page_config(page_title="Solana Dashboard (Minimal)", layout="centered")

st.title("Solana Morning Dashboard — Minimal")
st.caption("If you can see this, the app launched correctly. We’ll add more panels next.")

# Health
col1, col2 = st.columns(2)
with col1: st.success("✅ App booted")
with col2: st.write(f"Local time (UTC+4): {datetime.now(timezone(timedelta(hours=4))).strftime('%Y-%m-%d %H:%M')}")

st.divider()
st.subheader("Live Prices (CoinGecko)")
try:
    r = requests.get(
        "https://api.coingecko.com/api/v3/simple/price",
        params={"ids": "solana,ethereum", "vs_currencies": "usd", "include_24hr_change": "true"},
        timeout=6,
    )
    r.raise_for_status()
    js = r.json()
    sol, eth = js.get("solana", {}), js.get("ethereum", {})
    c1, c2 = st.columns(2)
    c1.metric("SOL (USD)", sol.get("usd","—"), f"{sol.get('usd_24h_change',0):.2f}% / 24h")
    c2.metric("ETH (USD)", eth.get("usd","—"), f"{eth.get('usd_24h_change',0):.2f}% / 24h")
except Exception as e:
    st.error(f"Price fetch failed (short timeout by design): {e}")
    st.info("Click 'Rerun' in the Streamlit menu or refresh the page.")
