from pymongo import MongoClient
from pymongo.server_api import ServerApi
import certifi
import pandas as pd
from tabulate import tabulate


# def test():
#     try:
#         client = MongoClient(
#             "mongodb+srv://odpp_user:Uu5VxTud3tkbklwT@atlascluster.aqrdbga.mongodb.net/?retryWrites=true&w=majority")
#         print("Available databases in mongo db: ")
#         print(client.list_database_names())
#         db = client.YouTubeDB
#         collection = db.phones
#         print(collection)
#     except Exception as e:
#         print(e)
#     else:
#         print("Test connection is successful")
#
# test()

print("in get content from mongo")
try:
    client = MongoClient(
        "mongodb+srv://odpp_user:Uu5VxTud3tkbklwT@atlascluster.aqrdbga.mongodb.net/?retryWrites=true&w=majority")

    print(client.list_database_names())
    db = client.youtube_db
    collection = db.transcripts
    data = pd.DataFrame(collection.find())
    #print(data.head(100))
    #data = data.head(50)

    #print(tabulate(data, headers='keys', tablefmt='psql'))
    print(data.shape)
except Exception as e:
    print(e)
