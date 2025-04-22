import streamlit as st

st.title("Crypto Position Size Calculator")

balance = st.number_input("Account Balance ($)", value=5000)
risk_pct = st.number_input("Risk % per Trade", value=2.0)
entry = st.number_input("Entry Price ($)", value=2000.0)
stop = st.number_input("Stop-Loss Price ($)", value=1950.0)

risk_amount = balance * (risk_pct / 100)
sl_distance = abs(entry - stop)
position_size = risk_amount / sl_distance if sl_distance else 0

st.write(f"**Risk Amount:** ${risk_amount:.2f}")
st.write(f"**Stop Loss Distance:** ${sl_distance:.2f}")
st.write(f"**Position Size:** {position_size:.6f} units")
