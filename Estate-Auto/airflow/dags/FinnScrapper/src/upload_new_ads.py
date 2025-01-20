import json
from pymongo import MongoClient
from pymongo.errors import BulkWriteError

def upload_new_ads(filtered_ad_data):
    with MongoClient('mongo', 27017) as client:
        db = client["Finn-database"]
        collection = db["estate-auto"]
        
        if len(filtered_ad_data) > 0:
            # Ensure the _id index is created before inserting
            collection.create_index("_id", unique=True)

            try:
                # Attempt to insert data
                collection.insert_many(filtered_ad_data, ordered=False)  # `ordered=False` skips duplicates
            except BulkWriteError as e:
                # Log or handle duplicate errors
                print("Some records already exist in the database:", e.details)

