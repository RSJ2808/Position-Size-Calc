import streamlit as st
import pandas as pd
from datetime import datetime

# --- Page Setup ---
st.set_page_config(page_title="Crypto Position Size Calculator", layout="centered")

st.markdown("""
    <style>
    .main {background-color: #0e1117;}
    .stApp {color: #f8f9fa;}
    </style>
""", unsafe_allow_html=True)

st.title("📈 Crypto Position Size Calculator")

# --- Calculator Inputs ---
balance = st.number_input("💰 Account Balance ($)", min_value=0.0, value=5000.0)
risk_pct = st.number_input("⚠️ Risk per Trade (%)", min_value=0.0, max_value=100.0, value=2.0)
entry = st.number_input("🎯 Entry Price ($)", min_value=0.0, value=2000.0)
stop = st.number_input("🛑 Stop-Loss Price ($)", min_value=0.0, value=1950.0)
take_profit = st.number_input("🚀 Take-Profit Price ($)", min_value=0.0, value=2100.0)
leverage = st.slider("🪙 Leverage (optional)", min_value=1, max_value=100, value=1)

# --- Trade Calculations ---
if entry > 0 and stop > 0 and stop != entry:
    risk_amount = balance * (risk_pct / 100)
    stop_loss_distance = abs(entry - stop)
    leveraged_risk_amount = risk_amount * leverage
    position_size = leveraged_risk_amount / stop_loss_distance

    # Profit & RRR
    potential_profit_per_unit = abs(take_profit - entry)
    total_profit = potential_profit_per_unit * position_size
    rrr = potential_profit_per_unit / stop_loss_distance if stop_loss_distance > 0 else 0

    st.markdown("### 🧮 Results")
    st.write(f"**Risk Amount:** ${risk_amount:.2f}")
    st.write(f"**Leverage Adjusted Risk:** ${leveraged_risk_amount:.2f}")
    st.write(f"**Stop Loss Distance:** ${stop_loss_distance:.2f}")
    st.write(f"**Position Size:** {position_size:.6f} units")
    st.write(f"**Potential Profit:** ${total_profit:.2f}")
    
    if rrr > 0:
        st.write(f"**Risk-to-Reward Ratio:** {rrr:.2f} : 1")
    else:
        st.warning("⚠️ Check your entry and take-profit values.")

# --- Trade Journal Section ---
st.markdown("---")
st.markdown("## 📝 Trade Journal")

# Initialize session state
if "journal" not in st.session_state:
    st.session_state.journal = []

with st.form("journal_form"):
    asset = st.text_input("Asset (e.g. BTC/USDT)")
    trade_date = st.date_input("Date", datetime.now().date())
    outcome = st.selectbox("Trade Outcome", ["Win", "Loss", "Breakeven"])
    notes = st.text_area("Notes")
    submitted = st.form_submit_button("📌 Save Trade")

    if submitted:
        st.session_state.journal.append({
            "Date": trade_date,
            "Asset": asset,
            "Entry": entry,
            "Stop": stop,
            "Take-Profit": take_profit,
            "RRR": round(rrr, 2) if 'rrr' in locals() else None,
            "Outcome": outcome,
            "Notes": notes
        })
        st.success("Trade saved to journal ✅")

# Display journal
if st.session_state.journal:
    st.markdown("### 📚 Trade History")
    df = pd.DataFrame(st.session_state.journal)
    st.dataframe(df, use_container_width=True)
