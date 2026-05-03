import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_option_menu import option_menu

# ----------------------------------
# PAGE CONFIG
# ----------------------------------
st.set_page_config(
    page_title="Smart Energy AI System",
    page_icon="⚡",
    layout="wide"
)

# ----------------------------------
# 🌈 ATTRACTIVE BACKGROUND UI
# ----------------------------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(-45deg, #0f172a, #1e293b, #0f172a, #1e293b);
    background-size: 400% 400%;
    animation: gradient 12s ease infinite;
}

@keyframes gradient {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Glass Card */
.card {
    background: rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    color: white;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
}

/* Titles */
h1, h2, h3 {
    color: white;
}

/* Buttons */
.stButton>button {
    background: #3b82f6;
    color: white;
    border-radius: 10px;
    height: 45px;
}

.stButton>button:hover {
    background: #2563eb;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------
# SESSION STATE
# ----------------------------------
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["Units_Used", "Bill"])

if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=["Month", "Units", "Bill"])

df = st.session_state.df
history = st.session_state.history

# ----------------------------------
# SIDEBAR MENU
# ----------------------------------
with st.sidebar:

    selected = option_menu(
        "⚡ Smart Energy AI",
        ["Dashboard", "Dataset Upload", "Bill Calculator", "Monthly Tracker", "Appliance Analysis", "Insights"],
        icons=["house", "upload", "calculator", "calendar", "plug", "graph-up"],
        default_index=0
    )

# ----------------------------------
# DASHBOARD (IMPROVED)
# ----------------------------------
if selected == "Dashboard":

    st.title("⚡ Smart Energy AI System")

    st.markdown("""
<div class="card">
<h3>💡 Smart Electricity Management System</h3>
✔ Upload Dataset  
✔ Real-time Bill Calculation  
✔ Monthly Tracking  
✔ Appliance Analysis  
✔ Smart Insights  
</div>
""", unsafe_allow_html=True)

    if len(df) > 0:

        col1, col2, col3 = st.columns(3)

        col1.markdown(f"<div class='card'><h3>Records</h3><h2>{len(df)}</h2></div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='card'><h3>Avg Units</h3><h2>{df['Units_Used'].mean():.2f}</h2></div>", unsafe_allow_html=True)
        col3.markdown(f"<div class='card'><h3>Avg Bill</h3><h2>₹{df['Bill'].mean():.2f}</h2></div>", unsafe_allow_html=True)

# ----------------------------------
# DATASET UPLOAD
# ----------------------------------
elif selected == "Dataset Upload":

    st.title("📂 Upload Dataset")

    file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

    if file is not None:

        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        st.session_state.df = df

        st.success("Dataset Loaded Successfully")
        st.dataframe(df)

        if "Units_Used" in df.columns and "Bill" in df.columns:

            fig = px.scatter(df, x="Units_Used", y="Bill", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

# ----------------------------------
# BILL CALCULATOR (IMPROVED)
# ----------------------------------
elif selected == "Bill Calculator":

    st.title("💡 Smart Bill Calculator")

    units = st.slider("Enter Units Consumed", 0, 1000, 100)

    def calc(u):

        if u <= 100:
            rate = 0
        elif u <= 300:
            rate = 3.5
        elif u <= 500:
            rate = 5
        else:
            rate = 7

        energy = u * rate
        fixed = 50
        tax = energy * 0.05
        total = energy + fixed + tax

        return energy, fixed, tax, total

    if st.button("Generate Bill"):

        e, f, t, total = calc(units)

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Energy", f"₹ {e:.2f}")
        col2.metric("Fixed", f"₹ {f:.2f}")
        col3.metric("Tax", f"₹ {t:.2f}")
        col4.metric("Total", f"₹ {total:.2f}")

        # 🔥 SMART TIP (NEW)
        if units > 500:
            st.error("⚠ High usage → Reduce AC usage & switch LED bulbs")
        elif units > 300:
            st.warning("⚡ Moderate usage → Turn off unused devices")
        else:
            st.success("✔ Efficient usage")

        fig = px.pie(names=["Energy", "Fixed", "Tax"],
                     values=[e, f, t],
                     title="Bill Breakdown")

        st.plotly_chart(fig)

# ----------------------------------
# MONTHLY TRACKER
# ----------------------------------
elif selected == "Monthly Tracker":

    st.title("📊 Monthly Tracker")

    month = st.text_input("Month")
    units = st.number_input("Units", min_value=0)
    bill = st.number_input("Bill", min_value=0.0)

    if st.button("Add Record"):

        new = pd.DataFrame([[month, units, bill]],
                           columns=["Month", "Units", "Bill"])

        st.session_state.history = pd.concat([history, new], ignore_index=True)

        st.success("Added!")

    if len(st.session_state.history) > 0:

        st.dataframe(st.session_state.history)

        fig = px.line(st.session_state.history, x="Month", y="Bill", markers=True)
        st.plotly_chart(fig)

# ----------------------------------
# APPLIANCE ANALYSIS
# ----------------------------------
elif selected == "Appliance Analysis":

    st.title("🔌 Appliance Usage Analyzer")

    ac = st.slider("AC Hours", 0, 24, 2)
    fan = st.slider("Fan Hours", 0, 24, 6)
    tv = st.slider("TV Hours", 0, 24, 3)

    if st.button("Analyze"):

        ac_u = ac * 1.5
        fan_u = fan * 0.075
        tv_u = tv * 0.2

        total = ac_u + fan_u + tv_u

        st.success(f"Daily Units: {total:.2f}")

        fig = px.pie(names=["AC", "Fan", "TV"],
                     values=[ac_u, fan_u, tv_u],
                     title="Usage Breakdown")

        st.plotly_chart(fig)

# ----------------------------------
# INSIGHTS
# ----------------------------------
elif selected == "Insights":

    st.title("📈 Smart Insights")

    if len(st.session_state.history) > 1:

        dfh = st.session_state.history

        fig = px.line(dfh, x="Month", y="Bill", markers=True)
        st.plotly_chart(fig)

        avg = dfh["Bill"].mean()
        last = dfh["Bill"].iloc[-1]

        if last > avg:
            st.error("⚠ Bill increasing trend detected")
        else:
            st.success("✔ Consumption stable")

    else:
        st.warning("Add monthly data first")