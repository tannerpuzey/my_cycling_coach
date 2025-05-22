import streamlit as st
import requests

# ─────────────────────────────
# Set Strava API credentials
CLIENT_ID = "160560"
CLIENT_SECRET = "ef5941bfe890ab58fddb1a1c71c3cfaef178b87c"
REDIRECT_URI = "https://mycyclingcoach-ybe9mpilksuvhtvwufvapc.streamlit.app"

# Build auth URL
auth_url = (
    f"https://www.strava.com/oauth/authorize?client_id={CLIENT_ID}"
    f"&response_type=code&redirect_uri={REDIRECT_URI}"
    f"&scope=read,activity:read_all&approval_prompt=force"
)

# ─────────────────────────────
# Streamlit UI

st.title("🚴 Tanner's AI Cycling Coach")

# Authentication Flow
if "code" not in st.query_params:
    st.write("To get started, connect your Strava account.")
    st.markdown(f"[🔗 Click here to connect your Strava account]({auth_url})", unsafe_allow_html=True)

else:
    code = st.query_params["code"][0]
    st.success("✅ Authorization code received!")

    response = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code"
        }
    )

    token_data = response.json()
    access_token = token_data.get("access_token")

    if access_token:
        st.success("✅ Access token acquired!")

        # Fetch recent activities
        st.subheader("📋 Your Recent Rides")

        headers = {"Authorization": f"Bearer {access_token}"}
        activities_url = "https://www.strava.com/api/v3/athlete/activities"
        params = {"per_page": 5, "page": 1}

        activity_response = requests.get(activities_url, headers=headers, params=params)

        st.write("Status code:", activity_response.status_code)
        st.write("Response text:", activity_response.text)

        if activity_response.status_code == 200:
            activities = activity_response.json()

            if activities:
                for activity in activities:
                    distance_km = activity['distance'] / 1000
                    st.markdown(f"**{activity['name']}** — {distance_km:.2f} km")
            else:
                st.info("No recent activities found.")

            # Simulated training metrics (for now)
            tss = 105
            ctl = 75
            atl = 82
            tsb = ctl - atl

            st.subheader("📊 Training Load Summary")
            st.metric("TSS", tss)
            st.metric("CTL", ctl)
            st.metric("ATL", atl)
            st.metric("TSB (Fatigue Index)", tsb)

            if tsb < -10:
                st.write("📉 You're likely fatigued. Consider a rest or easy recovery ride.")
            elif tsb > 10:
                st.write("💪 You're fresh! Time for some intervals or a hard climb.")
            else:
                st.write("😐 You're balanced. A steady endurance ride would be ideal today.")
        else:
            st.error("❌ Failed to fetch activities.")
            st.write(activity_response.text)

    else:
        st.error("❌ Failed to retrieve access token.")
        st.write(token_data)