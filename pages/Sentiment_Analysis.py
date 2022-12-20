import streamlit as st
import os, sys
from pymongo import MongoClient
import pandas as pd
from tabulate import tabulate
from nltk.tokenize import word_tokenize, sent_tokenize

from pymongo import MongoClient
import pandas as pd
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
from nltk.tokenize import word_tokenize, sent_tokenize

import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
import pandas as pd

# appending the parent directory path
# sys.path.append(r'C:\Users\a892215\Projects\ODPP\ODPP\visualization')
#
# # importing the methods
# from visualization.web_scraper_ifixit import get_content_from_mongo


st.set_page_config(page_title="Sentiment Analysis", page_icon="🌷")

st.markdown("# Sentiment Analysis 🌷")
st.sidebar.header("Sentiment Analysis")
st.write(
    """This page illustrates sentiment analysis results done with the [spaCy](https://spacy.io/usage/spacy-101) 
    library. SpaCy is a free, open-source library for advanced Natural Language Processing (NLP) in Python!"""
)


def load_data_youtube():
    print("in get content from mongo: youtube")
    try:
        client = MongoClient(
            "mongodb+srv://odpp_user:Uu5VxTud3tkbklwT@atlascluster.aqrdbga.mongodb.net/?retryWrites=true&w=majority")

        print(client.list_database_names())
        db = client.youtube_db
        collection = db.transcripts
        data = pd.DataFrame(collection.find())
        # print(data.head())
        # print(tabulate(data, headers='keys', tablefmt='psql'))

        transcript_texts = []
        for index in data.index.values:
            # print(data.iloc[index]["facts_doc"])
            transcript_text = data.iloc[index]["transcript_list"]
            transcript_text = '.'.join(transcript_text)
            transcript_texts.append(transcript_text)
        data["text"] = transcript_texts

        texts_reduced = []
        list = ['repair', 'healthy', 'battery', 'change', 'remove', 'removal', 'easy', 'hard', 'repair',
                'repairability']

        # for index in data.index.values:
        #     text = data.iloc[index]["text"]
        #
        #     sentences_with_word = []
        #     for sen in sent_tokenize(text):
        #         l = word_tokenize(sen)
        #
        #         if len(set(l).intersection(list)) > 0:
        #             sentences_with_word.append(sen)
        #     #print(sentences_with_word)
        #     texts_reduced.append(sentences_with_word)
        # data["text_reduced"] = texts_reduced

        for index in data.index.values:
            doc = data.loc[index, 'transcript_list']
            doc = ' '.join(doc)
            sentences_with_word = []
            for sen in sent_tokenize(doc):
                l = word_tokenize(sen)

                if len(set(l).intersection(list)) > 0:
                    sentences_with_word.append(sen)
            # print(sentences_with_word)
            texts_reduced.append(sentences_with_word)
        data["text_reduced"] = texts_reduced
        data_subset = data[['video_id', 'phone_name', 'text_reduced']]
        return data_subset
    except Exception as e:
        print(e)
    print("youtube data loaded successfully")


def get_ifixit_sentiment_data():
    pass


def get_df_sentiment(data):
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe('spacytextblob')
    phone_names = []
    sent_score = []
    sent_label = []
    total_pos = []
    total_neg = []

    for index in data.index.values:

        transcript = data.loc[index]["text_reduced"]
        phone_name = data.loc[index]["phone_name"]
        phone_names.append(phone_name)

        print(phone_name)
        print("i am in sentiment")
        # print(transcript)
        texts = " ".join(transcript)
        # print(texts)

        doc = nlp(texts)
        sentiment = doc._.blob.polarity
        sentiment = round(sentiment, 2)
        print("sentiment is")

        # doc = data_subset.loc[index, 'text_reduced']
        # #     doc = ' '.join(doc)
        # doc_new = nlp(doc)
        # sentiment = doc_new._.blob.polarity
        # sentiment = round(sentiment, 2)
        # print("sentiment is")

        print(sentiment)
        if sentiment > 0:
            label = "Positive"
        else:
            label = "Negative"

        sent_label.append(label)
        sent_score.append(sentiment)

        positive_words = []
        negative_words = []
        df_row = pd.DataFrame()
        df_final = pd.DataFrame()

        for x in doc._.blob.sentiment_assessments.assessments:
            if x[1] > 0:
                positive_words.append(x[0][0])
            elif x[1] < 0:
                negative_words.append(x[0][0])
            else:
                pass

        total_pos.append(', '.join(set(positive_words)))
        total_neg.append(', '.join(set(negative_words)))

        df_row = df_row.iloc[0:0]
        # print(df_row)
        # print(phone_name)
        # print(sent_score)
        # print(sent_label)

        df_row["Phone Name"] = phone_names
        df_row["Sentiment Score"] = sent_score
        df_row["Sentiment Label"] = sent_label
        df_row["Positive Words"] = total_pos
        df_row["Negative Words"] = total_neg
        # print(df_row)
        df_final = pd.concat([df_final, df_row], ignore_index=True)

    return df_final


def get_youtube_sentiment_data():
    data = load_data_youtube()
    phone_series = data['phone_name']
    no_dub = phone_series.drop_duplicates()
    p_list = no_dub.tolist()

    selection = st.sidebar.selectbox('Select a phone', [''] + p_list)
    print("Phone selected")

    # data_sentiment = data['text_reduced']
    # sentiment1_list = []

    # print(selection)
    df_sentiment = get_df_sentiment(data)

    df_selected = df_sentiment[df_sentiment['Phone Name'] == selection]
    st.subheader("Sentiment Analysis of " + selection)
    st.dataframe(df_selected[['Phone Name', 'Sentiment Score', 'Sentiment Label']])


def filter_by_selectbox():
    list = ["IFixIt", "YouTube"]
    selection = st.sidebar.selectbox('Select dataset to apply sentiment analysis on', [''] + list)
    print(selection)
    if selection == "IFixIt":
        get_ifixit_sentiment_data()
        st.subheader("in ifixit")
    if selection == "YouTube":
        get_youtube_sentiment_data()

st.subheader("Results")
st.write(
    """Our NLP analysis show done with SpaCy show us ..% corralated results with the sentiment scores from the IFixIt data.
    Keeping in mind that youtube transcript texts """
)

# data = load_data_youtube()
filter_by_selectbox()
# data = filter_by_selectbox(data)
