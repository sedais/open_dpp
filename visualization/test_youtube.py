from pymongo import MongoClient

# def get_transcripts(df_new, search_query, phone_name, page_token, search_type, num):
#     max_results = num
#     global API_COUNTER
#     print("beginning")
#     print(API_COUNTER)
#
#     # keys = ["AIzaSyBSuf1z7mqV9-2IH5WbIJzkrsM5b2KHBMU", "AIzaSyD5_DJ3nv9CySefqkEZH3jVEzzzewuwKbw",
#     #         "AIzaSyDwBns_kxeusJEy1iU1L5aDbQ0GvbCA2tg", "AIzaSyAwBN7ZnVlzHTiG9e3s7XyFOdXefcDYKnk",
#     #         "AIzaSyCMhPvzt2_lAOAsypiBCVJ2_uEivENlTIo", "AIzaSyCxd-fwKs1lKk1tGp5SG61sdGg4p8SEZ7s",
#     #         "AIzaSyDYRNQTPhPZm0R8nA_ivjJgFFwe9nCQfgY", "AIzaSyB2swKmvE7JYDdcUNgyYFJ1fLAFHu_Sfuk",
#     #         "AIzaSyAm-m5MYn2-wcnLCytHe_aUWgXFnwH7M6E", "AIzaSyB27pn1zUgB7lA2_vbkjDBoDZYuy7SP_l0"]
#
#     cols = ["phone_name", "video_id", "transcript_list"]
#     # df_transcripts = pd.DataFrame(columns=cols)
#
#     # df_transcripts = df
#     url = "https://www.googleapis.com/youtube/v3/search?key=" + api_key + "&q=" + search_query + "&type=" \
#           + search_type + "&part=snippet" + "&maxResults=1" + "&pageToken=" + page_token
#     response = requests.get(url).json()
#
#     next_page_token = response["nextPageToken"]
#     # api_counter = 0
#     while API_COUNTER <= max_results:
#         print("df shape")
#         print(df_new.shape[0])
#         if df_new.shape[0] == max_results:
#             print("max reached")
#             print(df_new)
#             return df_new
#             break
#             # write_transcripts_to_files(df_transcripts)
#         else:
#             if search_type == "video":
#                 for item in response['items']:
#                     # Option 1: save information in variables and add to dataframe
#                     video_id = item['id']['videoId']
#                     video_transcript = ""
#                     try:
#                         transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
#                         transcript_list = []
#                         for element in transcript:
#                             text = element['text']
#                             text += "."
#                             transcript_list.append(text)
#                     except Exception as e:
#                         print("Exception")
#
#                         transcript_list = []
#                     if not transcript_list:
#                         # list is empty
#                         get_transcripts(df_new, search_query, phone_name, next_page_token, search_type, max_results)
#                         print("list empty")
#                         print(API_COUNTER)
#                     else:
#                         print(video_id)
#                         print("list not empty")
#                         API_COUNTER += 1
#                         print(API_COUNTER)
#                         # print(transcript_list)
#                         cols = ["video_id", "phone_name", "transcript_list"]
#                         new_row = [video_id, phone_name, transcript_list]
#                         df_new_row = pd.DataFrame([new_row], columns=cols)
#                         df_new = pd.concat([df_new, df_new_row], ignore_index=True)
#                         print(df_new)
#                         print("in ")
#                         get_transcripts(df_new, search_query, phone_name, next_page_token, search_type, max_results)
#
#     # return df_transcripts
client = MongoClient(
    "mongodb+srv://odpp_user:Uu5VxTud3tkbklwT@atlascluster.aqrdbga.mongodb.net/?retryWrites=true&w=majority")
print("Available databases in mongo db: ")
print(client.list_database_names())
db = client.youtube_db
collection = db.transcripts
print(collection)

collection.delete_many({})
