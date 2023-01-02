import streamlit as st
from pymongo import MongoClient
from nltk.tokenize import word_tokenize, sent_tokenize
import pandas as pd

#from transformers import AutoTokenizer
#from transformers import AutoModelForSequenceClassification
#from scipy.special import softmax
#import spacy

st.set_page_config(page_title="Sentiment Analysis", page_icon="🌷")

st.markdown("# Sentiment Analysis 🌷")
st.sidebar.header("Sentiment Analysis")
st.write(
    """
    Sentiment analysis (also known as opinion mining or emotion AI) is a natural language processing (NLP) technique that identifies the polarity of a given text. [here](https://en.wikipedia.org/wiki/Sentiment_analysis) 
    Sentiment analysis allows companies to analyze data at scale, detect insights and automate processes and widely applied to reviews, survey responses and social media
    mentions to understand how people are talking about your brand vs your competitors.""")
st.write("""
    This page illustrates Social Media Sentiment Analysis Results of the transcript data retrieved from the YouTube API.
    Our Sentiment Analysis comprises results from three different NLP techniques
    
    1. **NLP with the** [spaCy](https://spacy.io/usage/spacy-101). SpaCy is a free, open-source library for advanced Natural Language Processing (NLP) in Python.
    
    2. **Google Cloud Platform Natural Language** [API](https://cloud.google.com/natural-language/docs/reference/libraries). Derives insights from unstructured text using Google machine learning.
    
    3. **Pre-trained Sentiment Analysis Model** from [Hugging Face Hub](https://huggingface.co/models)
            
        * [__Twitter-roberta-base-sentiment__](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment) is a roBERTa model trained on ~58M tweets and fine-tuned for sentiment analysis. Fine-tuning is the process of taking a pre-trained large language model (e.g. roBERTa in this case) and then tweaking it with additional training data to make it perform a second similar task (e.g. sentiment analysis).
            
        * [__SiEBERT - English-Language Sentiment Classification__](https://huggingface.co/siebert/sentiment-roberta-large-english) This model ("SiEBERT", prefix for "Sentiment in English") is a fine-tuned checkpoint of RoBERTa-large. It enables reliable binary sentiment analysis for various types of English-language text. For each instance, it predicts either positive (1) or negative (0) sentiment.
            
        """
         )

st.subheader("Results per Phone")
st.write(
    "To get the sentiment analysis results, please select either IFixIt or YouTube on the left hand side. In case of YouTube, additionally select a phone.")
st.write(
    "We have initially collected 132 phones from the IFixIt, and we analyze three YouTube videos for each phone in the database. *(For the demo purposes, this can be scaled up conveniently)*")


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


def get_spacy_results(data):
    print("in spacy")
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe('spacytextblob')
    phone_names = []
    sent_score = []
    sent_label = []
    total_pos = []
    total_neg = []

    for index in data.index.values:
        video_id = data.loc[index]["video_id"]
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


def get_df_sentiment(data):
    df_spacy = get_spacy_results(data)
    # get_gcp_results(data)
    return df_spacy


def load_youtube_sentiment_data():
    print("in get content from mongo: sentiment")
    try:
        client = MongoClient(
            "mongodb+srv://odpp_user:Uu5VxTud3tkbklwT@atlascluster.aqrdbga.mongodb.net/?retryWrites=true&w=majority")

        print(client.list_database_names())
        db = client.youtube_db
        collection = db.sentiment
        data = pd.DataFrame(collection.find())
        return data
    except Exception as e:
        print(e)
    print("sentiment data loaded successfully")

def get_youtube_sentiment_data():
    # data = load_data_youtube()
    data = load_youtube_sentiment_data()

    phone_series = data['Phone Name']
    no_dub = phone_series.drop_duplicates()
    p_list = no_dub.tolist()
    p_list_reversed = p_list.reverse()

    phone_selection = st.sidebar.selectbox('Select a phone', [''] + p_list)
    print("Phone selected")

    sentiment_types = ['All', 'spaCy', 'GCP', 'Roberta', 'Siebert']
    sentiment_selection = st.sidebar.selectbox('Select a sentiment analysis method', [''] + sentiment_types)
    print("Sentiment selected")

    # data_sentiment = data['text_reduced']
    # sentiment1_list = []

    # print(selection)
    print(data.columns)

    if sentiment_selection == 'All':
        df_sentiment = data[['Video Id', 'Phone Name', 'Spacy Label', 'Spacy Score','GCP Score', 'GCP Magnitude', 'Roberta Neg', 'Roberta Neu', 'Roberta Pos', 'Siebert Label', 'Siebert Score']]
        st.subheader(
            "Sentiment Analysis of first three videos of YouTube Teardown and Repair Assessment search for" + '\n' + phone_selection)
        st.dataframe(df_sentiment[df_sentiment['Phone Name'] == phone_selection])
    elif sentiment_selection == 'spaCy':
        df_sentiment = data[['Video Id', 'Phone Name', 'Spacy Label', 'Spacy Score']]
        st.subheader(
            "Sentiment Analysis of first three videos of YouTube Teardown and Repair Assessment search for" + '\n' + phone_selection)
        st.dataframe(df_sentiment[df_sentiment['Phone Name'] == phone_selection])
    elif sentiment_selection == 'GCP':
        df_sentiment = data[['Video Id', 'Phone Name', 'GCP Score', 'GCP Magnitude']]
        st.subheader(
            "Sentiment Analysis of first three videos of YouTube Teardown and Repair Assessment search for" + '\n' + phone_selection)
        st.dataframe(df_sentiment[df_sentiment['Phone Name'] == phone_selection])
    elif sentiment_selection == 'Roberta':
        df_sentiment = data[['Video Id', 'Phone Name', 'Roberta Neg', 'Roberta Neu', 'Roberta Pos']]
        st.subheader(
            "Sentiment Analysis of first three videos of YouTube Teardown and Repair Assessment search for" + '\n' + phone_selection)
        st.dataframe(df_sentiment[df_sentiment['Phone Name'] == phone_selection])
    elif sentiment_selection == 'Siebert':
        df_sentiment = data[['Video Id', 'Phone Name', 'Seiebert Label', 'Siebert Score']]
        st.subheader(
            "Sentiment Analysis of first three videos of YouTube Teardown and Repair Assessment search for" + '\n' + phone_selection)
        st.dataframe(df_sentiment[df_sentiment['Phone Name'] == phone_selection])

    #df_sentiment = get_df_sentiment(data)

    # df_selected = df_sentiment[df_sentiment['Phone Name'] == selection]
    # st.subheader("Sentiment Analysis of first three videos of YouTube Teardown and Repair Assessment search for" + '\n' + phone_selection)
    # st.dataframe(df_sentiment[df_sentiment['Phone Name'] == phone_selection])


def filter_by_selectbox():
    list = ["IFixIt", "YouTube"]
    selection = st.sidebar.selectbox('Select dataset to apply sentiment analysis on', [''] + list)
    print(selection)
    if selection == "IFixIt":
        get_ifixit_sentiment_data()
        st.subheader("in ifixit")
    if selection == "YouTube":
        get_youtube_sentiment_data()






data = load_youtube_sentiment_data()
filter_by_selectbox()
# data = filter_by_selectbox(data)


st.subheader("End Results")
st.write("""    
Our NLP analysis shows corralated results with the sentiment scores from the IFixIt data. Keeping in mind that YouTube transcript texts with poorly created video captions can damage the video’s message through inaccuracy.
 """
)

st.write(""" **Challenges** 
AutoCaptioning: As YouTube generate automatic captions, it combines Google's automated speech recognition technology with its own subtitling system including automatic speech recognition (ASR) technology to generate auto captions.
""")

st.write("""**Takeaway from the challenge:** Automatic speech recognition software has become more sophisticated, but the quality of the video captions can still vary widely.
""")


st.write("**1. SpaCy** Top 5 Phones")
df_spacy_top_5 = data.groupby('Phone Name')['Spacy Score'].mean().to_frame()
df_spacy_top_5 = df_spacy_top_5.sort_values(by='Spacy Score', ascending=False)
st.dataframe(df_spacy_top_5.head(5))

st.write("**2. GCP** Top 5 Phones")
df_gcp_top_5 = data.groupby('Phone Name')['GCP Score'].mean().to_frame()
df_gcp_top_5 = df_gcp_top_5.sort_values(by='GCP Score', ascending=False)
st.dataframe(df_gcp_top_5.head(5))

st.write("**3. Roberta** Top 5 Phones")
df_roberta_top_5 = data.groupby('Phone Name')['Roberta Pos'].mean().to_frame()
df_roberta_top_5 = df_roberta_top_5.sort_values(by='Roberta Pos', ascending=False)
st.dataframe(df_roberta_top_5.head(5))

st.write("**4. Siebert** Top 5 Phones")
df_siebert_top_5 = data.groupby('Phone Name')['Siebert Score'].mean().to_frame()
df_siebert_top_5 = df_siebert_top_5.sort_values(by='Siebert Score', ascending=False)
st.dataframe(df_siebert_top_5.head(5))