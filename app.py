import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="Mistake AI Pro", layout="centered")

st.title("🧠 Mistake Pattern Analyzer AI — PRO LEVEL")

# ---------------- SIDEBAR ----------------
page = st.sidebar.selectbox(
    "Choose Section",
    ["Dashboard", "Analysis", "Progress", "AI Feedback"]
)

# ---------------- LOAD DATA ----------------
df = pd.read_csv("data.csv")
wrong = df[df["Status"] == "Wrong"]

# ---------------- CALCULATIONS ----------------
total = len(df)
correct = len(df[df["Status"] == "Correct"])
score = (correct / total) * 100

# ---------------- LOAD HISTORY ----------------
history_file = "history.csv"

try:
    history = pd.read_csv(history_file)
except:
    history = pd.DataFrame(columns=["Date","Score","Wrong","Correct"])

# =========================================================
# ---------------- DASHBOARD ----------------
# =========================================================
if page == "Dashboard":
    st.subheader("🏆 Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("📊 Total Questions", total)
    col2.metric("✅ Correct", correct)
    col3.metric("❌ Wrong", len(wrong))

    st.metric("🎯 Accuracy", f"{score:.2f}%")

    st.markdown("---")

    st.subheader("📋 Dataset Preview")
    st.dataframe(df)

# =========================================================
# ---------------- ANALYSIS ----------------
# =========================================================
elif page == "Analysis":
    st.subheader("📊 Mistake Analysis")

    col1, col2 = st.columns(2)

    # Table
    with col1:
        st.write("Error Count")
        st.write(wrong["ErrorType"].value_counts())

    # Graph
    with col2:
        fig, ax = plt.subplots()
        wrong["ErrorType"].value_counts().plot(kind="bar", ax=ax)
        ax.set_title("Mistake Distribution")
        st.pyplot(fig)

# =========================================================
# ---------------- PROGRESS ----------------
# =========================================================
elif page == "Progress":
    st.subheader("📈 Progress Tracking")

    if st.button("💾 Save Today's Progress"):
        new_data = pd.DataFrame([{
            "Date": str(datetime.date.today()),
            "Score": score,
            "Wrong": len(wrong),
            "Correct": correct
        }])

        history = pd.concat([history, new_data], ignore_index=True)
        history.to_csv(history_file, index=False)
        st.success("Saved!")

    if len(history) > 0:
        fig, ax = plt.subplots()
        ax.plot(history["Date"], history["Score"], marker="o")
        ax.set_title("Performance Trend")
        ax.set_ylabel("Accuracy %")
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

    st.dataframe(history)

# =========================================================
# ---------------- AI FEEDBACK ----------------
# =========================================================
elif page == "AI Feedback":
    st.subheader("🧠 AI Feedback")

    if len(wrong) > 0:
        top_error = wrong["ErrorType"].value_counts().idxmax()
        weak_topic = df.groupby("Topic")["Status"].apply(
            lambda x: (x == "Correct").mean() * 100
        ).idxmin()

        st.error(f"🔴 Main Issue: {top_error}")
        st.info(f"📚 Weak Topic: {weak_topic}")

        st.markdown("### 🎯 Recommendation")

        if top_error == "Concept":
            st.warning("Focus on theory revision and concept clarity.")

        elif top_error == "Careless":
            st.warning("Slow down and double-check answers.")

        elif top_error == "Silly":
            st.warning("Improve attention to detail.")

        st.success("💡 Tip: Practice consistently for improvement!")

    else:
        st.success("No mistakes found 🎉")