import streamlit as st

# Title and welcome
st.title("🚴 Tanner's AI Cycling Coach")
st.write("Welcome! Here's your personalized cycling dashboard.")

# Simulated training metrics
tss = 105   # Training Stress Score
ctl = 75    # Chronic Training Load
atl = 82    # Acute Training Load
tsb = ctl - atl  # Training Stress Balance

# Display metrics
st.metric("TSS", tss)
st.metric("CTL", ctl)
st.metric("ATL", atl)
st.metric("TSB (Fatigue Index)", tsb)

# Simple recommendation logic
if tsb < -10:
    st.write("📉 You're likely fatigued. Consider a rest or easy recovery ride.")
elif tsb > 10:
    st.write("💪 You're fresh! Time for some intervals or a hard climb.")
else:
    st.write("😐 You're balanced. A steady endurance ride would be ideal today.")