import streamlit as st
import pandas as pd

st.set_page_config(page_title="YouTube Trend Analyzer", layout="wide")

st.title("YouTube Trend Analyzer (India)")

# Create tabs
tab1, tab2 = st.tabs(["📊 Analytics", "💡 Video Idea Generator"])
st.write("Insights from YouTube trending data to help creators understand what content performs best.")

# Load datasets
categories = pd.read_csv("data/trending_categories_india.csv")
upload_hour = pd.read_csv("data/best_upload_hour_india.csv")
upload_day = pd.read_csv("data/best_upload_day_india.csv")
video_duration = pd.read_csv("data/best_video_duration_india.csv")
keywords = pd.read_csv("data/trending_keywords_india.csv")

with tab1:
    st.header("Trending Video Categories")
    st.bar_chart(categories.set_index(categories.columns[0]))


    st.header("Best Upload Time")
    st.subheader("Best Upload Hour")
    st.bar_chart(upload_hour.set_index(upload_hour.columns[0]))


    st.subheader("Best Upload Day")
    st.bar_chart(upload_day.set_index(upload_day.columns[0]))


    st.header("Best Video Duration")
    st.bar_chart(video_duration.set_index(video_duration.columns[0]))

    st.header("Trending Keywords")
    st.bar_chart(keywords.set_index("keyword"))


with tab2:

    st.header("YouTube Video Idea Generator")

    topic = st.text_input("Enter a topic you want to create a video about")

    if topic:

        topic = topic.lower()

        if "gaming" in topic:
            st.write("Trending Gaming Ideas:")
            st.write("- Minecraft Challenge")
            st.write("- GTA Franklin Story Mode")
            st.write("- Granny Horror Gameplay")

        elif "movie" in topic or "film" in topic:
            st.write("Trending Movie Content Ideas:")
            st.write("- Trailer Reaction")
            st.write("- Movie Teaser Breakdown")
            st.write("- Song Reaction")

        elif "short" in topic:
            st.write("Trending Shorts Ideas:")
            st.write("- Quick Comedy Skits")
            st.write("- Viral VS Challenge")
            st.write("- Fast Reaction Videos")

        else:
            st.write("General Trending Ideas:")
            st.write("- Reaction Video")
            st.write("- Live Stream")
            st.write("- VS Challenge")    