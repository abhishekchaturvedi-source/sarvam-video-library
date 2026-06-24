import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Sarvam Video Library",
    layout="wide"
)

st.title("🎥 Sarvam Video Library")

# Read Excel
df = pd.read_excel("VideoList.xlsx")

# Remove blanks
df = df.fillna("")

# Batch
batch = st.selectbox(
    "Select Batch",
    sorted(df["Batch"].unique())
)

# Subject
subjects = sorted(
    df[df["Batch"] == batch]["Subject"].unique()
)

subject = st.selectbox(
    "Select Subject",
    subjects
)

# Faculty
faculties = sorted(
    df[
        (df["Batch"] == batch)
        &
        (df["Subject"] == subject)
    ]["Faculty"].unique()
)

faculty = st.selectbox(
    "Select Faculty",
    faculties
)

# Chapter
chapters = sorted(
    df[
        (df["Batch"] == batch)
        &
        (df["Subject"] == subject)
        &
        (df["Faculty"] == faculty)
    ]["Chapter"].unique()
)

chapter = st.selectbox(
    "Select Chapter",
    chapters
)

# Videos
videos = df[
    (df["Batch"] == batch)
    &
    (df["Subject"] == subject)
    &
    (df["Faculty"] == faculty)
    &
    (df["Chapter"] == chapter)
]

st.divider()

st.subheader("Videos")

for i, row in videos.iterrows():

    with st.expander(row["Video Name"]):

        st.markdown(
            f"[▶ Open Video]({row['Video URL']})"
        )

        if row["Embed URL"] != "":
            st.components.v1.iframe(
                row["Embed URL"],
                height=500,
                scrolling=False
            )
