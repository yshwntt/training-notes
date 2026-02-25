import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
import datetime as dt  # using this for today date

# ---------------------------
# Connect to MySQL database
# ---------------------------

# Connecting to MySQL (change password)
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="yASH@3633",
    database="productivity_app"
)

# cursor used to run SQL commands
cursor = conn.cursor()

# Creating table if it does not exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date VARCHAR(20),
    study_hours FLOAT,
    total_screen_time FLOAT,
    earned_points INT,
    earned_minutes INT
)
""")
conn.commit()

# Creating two tabs (1st tab analysis, 2nd tab application)
tab1, tab2 = st.tabs([" Analysis", " Application"])


# ---------------------------
# TAB 1: ANALYSIS
# ---------------------------
with tab1:
    st.title("Dataset Analysis")

    # Loading dataset (make sure this file exists in data folder)
    data_path = "data/student_productivity.csv"
    df = pd.read_csv(data_path)

    # Showing basic details
    st.write("### Dataset Shape")
    st.write(df.shape)

    st.write("### First 5 Rows")
    st.dataframe(df.head())

    # Checking missing values and duplicates (basic cleaning check)
    st.write("### Missing Values (should be 0)")
    st.dataframe(df.isnull().sum())

    st.write("### Duplicate Rows Count")
    st.write(df.duplicated().sum())

    st.divider()

    # Creating total screen time column (same as I did in notebook)
    df["total_screen_time"] = (
        df["phone_usage_hours"]
        + df["social_media_hours"]
        + df["youtube_hours"]
        + df["gaming_hours"]
    )

    # Removing unrealistic values (> 24 hours) because a day has only 24 hours
    df_clean = df[df["total_screen_time"] <= 24].copy()

    st.write("### Cleaned Dataset Shape (after removing >24 screen time)")
    st.write(df_clean.shape)

    st.divider()

    # Correlations (same results we calculated before)
    st.write("## Correlation Results")

    # Study vs Productivity (this was strongest)
    corr_study_prod = df_clean["study_hours_per_day"].corr(df_clean["productivity_score"])
    st.write("Study Hours vs Productivity Score =", round(corr_study_prod, 4))

    # Screen vs Productivity (negative relation)
    corr_screen_prod = df_clean["total_screen_time"].corr(df_clean["productivity_score"])
    st.write("Total Screen Time vs Productivity Score =", round(corr_screen_prod, 4))

    st.divider()

    # Scatter Plot 1: Study vs Productivity
    st.write("## Scatter Plot: Study Hours vs Productivity")
    fig1, ax1 = plt.subplots()
    ax1.scatter(df_clean["study_hours_per_day"], df_clean["productivity_score"])
    ax1.set_xlabel("Study Hours Per Day")
    ax1.set_ylabel("Productivity Score")
    st.pyplot(fig1)

    # Scatter Plot 2: Screen Time vs Productivity
    st.write("## Scatter Plot: Screen Time vs Productivity")
    fig2, ax2 = plt.subplots()
    ax2.scatter(df_clean["total_screen_time"], df_clean["productivity_score"])
    ax2.set_xlabel("Total Screen Time")
    ax2.set_ylabel("Productivity Score")
    st.pyplot(fig2)

    # Small summary 
    st.write("## My Findings")
    st.write("""
    - Study hours strongly increase productivity.
    - Total screen time reduces productivity.
    - This supports my idea: reward productive work and limit scrolling.
    """)

    st.divider()

    # Showing saved records also in Analysis tab
    st.write("## Saved Records From MySQL (Logs Table)")

    # Reading from database and showing it
    logs_df = pd.read_sql("SELECT * FROM user_logs ORDER BY id DESC", conn)
    st.dataframe(logs_df)


# ---------------------------
# TAB 2: APPLICATION
# ---------------------------
with tab2:
    st.title("Productivity Paywall (Rule-Based)")
    st.write("You earn social media minutes based on productive activities.")

    # Taking inputs from user
    study_hours = st.number_input("Study hours today", 0.0, 12.0, 2.0, 0.5)

    # Taking screen time components separately (same as dataset columns)
    phone = st.number_input("Phone usage (hours)", 0.0, 24.0, 3.0, 0.5)
    social = st.number_input("Social media (hours)", 0.0, 24.0, 2.0, 0.5)
    youtube = st.number_input("YouTube (hours)", 0.0, 24.0, 1.0, 0.5)
    gaming = st.number_input("Gaming (hours)", 0.0, 24.0, 0.0, 0.5)

    # Calculating total screen time
    total_screen_time = phone + social + youtube + gaming
    st.info(f"Total screen time = {total_screen_time:.1f} hours")

    # Basic validation (screen time can't exceed 24)
    if total_screen_time > 24:
        st.error("Total screen time cannot be more than 24 hours. Please correct inputs.")
        st.stop()

    st.divider()



    # Study reward using loop
    study_points = 0

    for hour in range(int(study_hours)):
        study_points += 50

    # half hour bonus
    if study_hours % 1 != 0:
        study_points += 25

    # Screen time penalty
    penalty = 0

    if total_screen_time > 6:
        extra_time = total_screen_time - 6
        full_hours = int(extra_time)

        for hour in range(full_hours):
            penalty += 10

        # half hour penalty
        if extra_time % 1 != 0:
            penalty += 5

    # Final points (cannot go below zero)
    points = max(0, study_points - penalty)

    # Convert to minutes
    social_minutes = int(points * 0.5)

    # Showing result
    st.subheader("Result")
    st.write("Points earned =", int(points))
    st.write("Social media minutes unlocked =", social_minutes)

    st.write("### Why this rule?")
    st.write("""
    - Study hours increases productivity (strong positive correlation).
    - Screen time reduces productivity (negative correlation).
    - So the app rewards study and penalizes high screen time.
    """)

    st.divider()

    # ---------------------------
    # SAVE TO DATABASE BUTTON
    # ---------------------------

    today_date = dt.date.today().strftime("%Y-%m-%d")

    if st.button("Save to Database"):
        cursor.execute("""
            INSERT INTO user_logs (date, study_hours, total_screen_time, earned_points, earned_minutes)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            today_date,
            float(study_hours),
            float(total_screen_time),
            int(points),
            int(social_minutes)
        ))

        conn.commit()
        st.success("Saved successfully to MySQL!")

    st.divider()

    # ---------------------------
    # SHOW SAVED RECORDS
    # ---------------------------

    st.subheader("Saved Records (From MySQL)")

    logs_df = pd.read_sql("SELECT * FROM user_logs ORDER BY id DESC", conn)
    st.dataframe(logs_df)

    st.divider()

    # ---------------------------
    # DELETE ALL RECORDS
    # ---------------------------

    if st.button("Delete All Records"):
        cursor.execute("DELETE FROM user_logs")
        conn.commit()
        st.warning("All records deleted from database.")