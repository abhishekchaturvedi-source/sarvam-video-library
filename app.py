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

df = load_data()
# ======================
# ======================
# HEADER
# ======================

# ======================
# HEADER
# ======================

col1, col2, col3 = st.columns([1, 8, 1])

with col1:
    st.image("assets/logo.png", width=450)

with col2:
    st.markdown(
        """
        <h1 style="
            text-align:center;
            color:#0B5ED7;
            margin-top:20px;
            margin-bottom:0px;
            font-weight:bold;">
            🎥 Sarvam Video Library
        </h1>

        <p style="
            text-align:center;
            color:gray;
            font-size:18px;
            margin-top:0px;">
            Faculty Lecture Verification Portal
        </p>
        """,
        unsafe_allow_html=True
    )
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

            st.write("▶ Embedded Player")

      with col2:

    if row["Embed URL"] != "":

        embed_url = get_embed_url(row["Embed URL"])

        if embed_url:

            components.html(
                f"""
                <iframe
                    src="{embed_url}"
                    width="100%"
                    height="500"
                    frameborder="0"
                    allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media"
                    allowfullscreen>
                </iframe>
                """,
                height=520,
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

# -----------------------
# Lecture Navigation
# -----------------------

lecture_list = videos["Video Name"].tolist()

# Create session state
if "current_index" not in st.session_state:
    st.session_state.current_index = 0

# Reset index when chapter changes
chapter_key = f"{batch}_{subject}_{faculty}_{chapter}"

if "last_chapter" not in st.session_state:
    st.session_state.last_chapter = chapter_key

if st.session_state.last_chapter != chapter_key:
    st.session_state.current_index = 0
    st.session_state.last_chapter = chapter_key

# Lecture dropdown
selected_lecture = st.selectbox(
    "Lecture",
    lecture_list,
    index=st.session_state.current_index
)

st.session_state.current_index = lecture_list.index(selected_lecture)

# Previous / Next buttons
col1, col2, col3 = st.columns([1,4,1])

with col1:
    if st.button("⬅ Previous"):
        if st.session_state.current_index > 0:
            st.session_state.current_index -= 1
            st.rerun()

with col3:
    if st.button("Next ➡"):
        if st.session_state.current_index < len(lecture_list)-1:
            st.session_state.current_index += 1
            st.rerun()

lecture = lecture_list[st.session_state.current_index]

row = videos[videos["Video Name"] == lecture].iloc[0]

st.markdown(
    f"### 🎬 Lecture {st.session_state.current_index + 1} of {len(lecture_list)}"
)

st.markdown(f"## {row['Video Name']}")

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
