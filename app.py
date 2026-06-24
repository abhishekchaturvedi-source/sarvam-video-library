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
@st.cache_data
def load_data():
    data = pd.read_excel(
        "VideoList.xlsx",
        dtype=str
    )

    data = data.fillna("")

    return data

df = load_data()

st.title("🎥 Sarvam Video Library")

# ======================
# GLOBAL SEARCH
# ======================
st.sidebar.header("🔍 Search Entire Library")

search_text = st.sidebar.text_input(
    "Search Lecture / Chapter / Faculty"
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
                    components.iframe(
                        row["Embed URL"],
                        height=500,
                        scrolling=False
                    )

    st.stop()


# ======================
# SIDEBAR FILTERS
# ======================

st.sidebar.header("Filters")

batch = st.sidebar.selectbox(
    "Batch",
    sorted(df["Batch"].unique())
)

subject = st.sidebar.selectbox(
    "Subject",
    sorted(
        df[df["Batch"] == batch]["Subject"].unique()
    )
)

faculty = st.sidebar.selectbox(
    "Faculty",
    sorted(
        df[
            (df["Batch"] == batch)
            &
            (df["Subject"] == subject)
        ]["Faculty"].unique()
    )
)

chapter = st.sidebar.selectbox(
    "Chapter",
    sorted(
        df[
            (df["Batch"] == batch)
            &
            (df["Subject"] == subject)
            &
            (df["Faculty"] == faculty)
        ]["Chapter"].unique()
    )
)

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

for _, row in videos.iterrows():

    with st.container(border=True):

        st.markdown(f"### 🎬 {row['Video Name']}")

        col1, col2 = st.columns([1,5])

        with col1:

            st.link_button(
                "▶ Open Vimeo",
                row["Video URL"]
            )

        with col2:

            if row["Embed URL"] != "":

                st.components.v1.iframe(
                    row["Embed URL"],
                    height=500,
                    scrolling=False
                )