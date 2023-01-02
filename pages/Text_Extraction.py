import streamlit as st

st.set_page_config(page_title="Text Extraction", page_icon=" 🔑")

st.markdown("# Text Extraction 🔑")
st.sidebar.header("Text Extraction")
st.write(
    """This pages illustrates the result of text extraction analysis done with the [KeyBERT](https://towardsdatascience.com/enhancing-keybert-keyword-extraction-results-with-keyphrasevectorizers-3796fa93f4db)
     KeyBERT is an easy-to-use Python package for keyphrase extraction with BERT language models."""
)



# Using object notation
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )