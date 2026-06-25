import re
import html

def get_embed_url(embed_html):
    if pd.isna(embed_html):
        return ""

    match = re.search(r'src="([^"]+)"', str(embed_html))

    if match:
        return html.unescape(match.group(1))

    return ""
import streamlit.components.v1 as components
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Sarvam Video Library",
    page_icon="🎥",
    layout="wide"
)

# --------------------------
# Load Data
# --------------------------
# --------------------------
# Load Data
# --------------------------
@st.cache_data(ttl=60)
def load_data():
    df = pd.read_excel(
        "VideoLists.xlsx",
        dtype=str
    ).fillna("")
    return df

df = load_data()# ======================
# GLOBAL SEARCH
# ======================
# ======================
# TOP SEARCH
# ======================

st.markdown("### 🔍 Search")

search_text = st.text_input(
    "Search",
    label_visibility="collapsed",
    placeholder="Search Lecture / Chapter / Faculty..."
)

if search_text:

    result = df[
        df["Video Name"].str.contains(search_text, case=False, na=False)
        |
        df["Chapter"].str.contains(search_text, case=False, na=False)
        |
        df["Faculty"].str.contains(search_text, case=False, na=False)
    ]

    st.subheader(f"Search Results ({len(result)})")

    for _, row in result.iterrows():

        with st.expander(row["Video Name"]):

            col1, col2 = st.columns([1,3])

            with col1:
                st.link_button("▶ Open Vimeo", row["Video URL"])

            with col2:

                if row["Embed URL"] != "":

                    embed_url = get_embed_url(row["Embed URL"])

                    if embed_url:
                        st.iframe(
                            embed_url,
                            height=500,
                            scrolling=False
                        )

    st.stop()


# ======================
# ======================
# TOP FILTERS
# ======================

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

# ---------------- Batch ----------------

batch_values = ["Select Batch"] + sorted(df["Batch"].unique())

with col1:
    batch = st.selectbox(
        "Batch",
        batch_values,
        index=0
    )

# ---------------- Subject ----------------

if batch == "Select Batch":
    subject_values = ["Select Subject"]
else:
    subject_values = ["Select Subject"] + sorted(
        df[df["Batch"] == batch]["Subject"].unique()
    )

with col2:
    subject = st.selectbox(
        "Subject",
        subject_values,
        index=0
    )

# ---------------- Faculty ----------------

if subject == "Select Subject":
    faculty_values = ["Select Faculty"]
else:
    faculty_values = ["Select Faculty"] + sorted(
        df[
            (df["Batch"] == batch)
            &
            (df["Subject"] == subject)
        ]["Faculty"].unique()
    )

with col3:
    faculty = st.selectbox(
        "Faculty",
        faculty_values,
        index=0
    )

# ---------------- Chapter ----------------

if faculty == "Select Faculty":
    chapter_values = ["Select Chapter"]
else:
    chapter_values = ["Select Chapter"] + sorted(
        df[
            (df["Batch"] == batch)
            &
            (df["Subject"] == subject)
            &
            (df["Faculty"] == faculty)
        ]["Chapter"].unique()
    )

with col4:
    chapter = st.selectbox(
        "Chapter",
        chapter_values,
        index=0
    )

# Wait until user selects everything

if batch == "Select Batch":
    st.stop()

if subject == "Select Subject":
    st.stop()

if faculty == "Select Faculty":
    st.stop()

if chapter == "Select Chapter":
    st.stop()
# ======================
# CHAPTER VIDEOS
# ======================

videos = df[
    (df["Batch"] == batch)
    &
    (df["Subject"] == subject)
    &
    (df["Faculty"] == faculty)
    &
    (df["Chapter"] == chapter)
]

st.subheader(f"📚 {chapter}")

search_inside = st.text_input(
    "Search within this chapter"
)

if search_inside:
    videos = videos[
        videos["Video Name"].str.contains(
            search_inside,
            case=False,
            na=False
        )
    ]

st.write(f"Total Videos : {len(videos)}")

# ======================
# VIDEO LIST
# ======================

lecture = st.selectbox(
    "Lecture",
    videos["Video Name"].tolist(),
    index=0
)

row = videos[videos["Video Name"] == lecture].iloc[0]

st.markdown(f"## 🎬 {row['Video Name']}")

embed_url = get_embed_url(row["Embed URL"])

if embed_url:
    st.components.v1.html(
        f"""
        <iframe
            src="{embed_url}"
            width="100%"
            height="700"
            frameborder="0"
            allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media"
            allowfullscreen>
        </iframe>
        """,
        height=720,
    )
