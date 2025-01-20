from pymongo import MongoClient

def check_existing_ads(processed_ad_data):
    # Handle missing '_id' keys
    new_finn_id = [data["_id"] for data in processed_ad_data if "_id" in data]

    with MongoClient('mongo', 27017) as client:
        db = client["finn_database"]
        collection = db["estate-auto"]

        # Fetch existing IDs from the database
        existing_finn_id = [doc["_id"] for doc in collection.find({}, {'_id': True})]

    # Find duplicates using set intersection
    duplicates = set(new_finn_id).intersection(existing_finn_id)

    # Filter out data already in the database
    filtered_ad_data = [data for data in processed_ad_data if data.get("_id") not in duplicates]

    return filtered_ad_data
