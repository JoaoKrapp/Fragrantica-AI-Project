from pymongo import MongoClient


def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   # Put your mongo database link here
   CONNECTION_STRING = "YOUR_DATABASE"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   db = MongoClient(CONNECTION_STRING)['perfume']
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return db

   


  
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__": 
   db = get_database()
   db['brands'].insert_one({"teste" : 1})