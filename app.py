import streamlit as st
import pandas as pd
import re
import html

st.set_page_config(
    page_title="Sarvam Video Library",
    page_icon="🎥",
    layout="wide"
)


# ----------------------
# Extract Vimeo Embed URL
# ----------------------
def get_embed_url(embed_html):
    if pd.isna(embed_html):
        return ""

    text = str(embed_html)

    match = re.search(r'src="([^"]+)"', text)

    if match:
        return html.unescape(match.group(1))

    return ""


# ----------------------
# Load Excel
# ----------------------
@st.cache_data
def load_data():
    return pd.read_excel("VideoList.xlsx", dtype=str).fillna("")


df = load_data()

st.title("🎥 Sarvam Video Library")


# ----------------------
# Global Search
# ----------------------
search = st.sidebar.text_input(
    "🔍 Search Lecture / Chapter / Faculty"
)

if search:

    result = df[
        df["Video Name"].str.contains(search, case=False, na=False)
        |
        df["Chapter"].str.contains(search, case=False, na=False)
        |
        df["Faculty"].str.contains(search, case=False, na=False)
    ]

else:
    result = df


# ----------------------
# Filters
# ----------------------
batch = st.sidebar.selectbox(
    "Batch",
    sorted(result["Batch"].unique())
)

subject = st.sidebar.selectbox(
    "Subject",
    sorted(
        result[result["Batch"] == batch]["Subject"].unique()
    )
)

faculty = st.sidebar.selectbox(
    "Faculty",
    sorted(
        result[
            (result["Batch"] == batch)
            &
            (result["Subject"] == subject)
        ]["Faculty"].unique()
    )
)

chapter = st.sidebar.selectbox(
    "Chapter",
    sorted(
        result[
            (result["Batch"] == batch)
            &
            (result["Subject"] == subject)
            &
            (result["Faculty"] == faculty)
        ]["Chapter"].unique()
    )
)


videos = result[
    (result["Batch"] == batch)
    &
    (result["Subject"] == subject)
    &
    (result["Faculty"] == faculty)
    &
    (result["Chapter"] == chapter)
].reset_index(drop=True)


st.subheader(chapter)

video_names = videos["Video Name"].tolist()

selected_video = st.selectbox(
    "Select Lecture",
    video_names
)

index = video_names.index(selected_video)

row = videos.iloc[index]

embed_url = get_embed_url(row["Embed URL"])

# ----------------------
# Navigation Buttons
# ----------------------
col1, col2, col3, col4 = st.columns([1,1,1,3])

with col1:
    if index > 0:
        if st.button("◀ Previous"):
            st.session_state.selected = index - 1

with col2:
    st.link_button(
        "🔗 Vimeo",
        row["Video URL"]
    )

with col3:
    st.code(row["Video URL"])

st.divider()

st.markdown(
    f"### 🎬 {row['Video Name']}"
)

if embed_url:
    st.components.v1.html(
        f"""
        <iframe
            src="{embed_url}"
            width="100%"
            height="700"
            frameborder="0"
            allow="autoplay; fullscreen; picture-in-picture"
            allowfullscreen>
        </iframe>
        """,
        height=720
    )
else:
    st.error("Embed URL not found")
