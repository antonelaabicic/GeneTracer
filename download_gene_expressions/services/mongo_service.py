# from pymongo import MongoClient

# # MongoDB Configuration
# MONGO_URI = "mongodb://localhost:27017"
# DATABASE_NAME = "gene_tracer"
# COLLECTION_NAME = "gene_data"

# # Initialize MongoDB client
# mongo_client = MongoClient(MONGO_URI)
# db = mongo_client[DATABASE_NAME]
# collection = db[COLLECTION_NAME]

# # Insert data into MongoDB
# def insert_gene_data(data):
#     """
#     Inserts a dictionary representing gene data into the MongoDB collection.
#     """
#     result = collection.insert_one(data)
#     print(f"Inserted document with ID: {result.inserted_id}")

