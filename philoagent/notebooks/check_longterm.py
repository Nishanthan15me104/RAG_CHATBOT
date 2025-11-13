import pymongo

# MongoDB connection URI from your logs
MONGO_URI = "mongodb://philoagents:philoagents@localhost:27017/?directConnection=true"

# The name of the database and collection
DB_NAME = "philoagents"
COLLECTION_NAME = "philosopher_long_term_memory"

def check_database():
    """Connects to MongoDB and prints the document count in the specified collection."""
    client = None
    try:
        # Connect to the MongoDB instance
        print("Attempting to connect to MongoDB...")
        client = pymongo.MongoClient(MONGO_URI)
        
        # Get the database and collection
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        
        print(f"Connected to database: '{DB_NAME}'")
        print(f"Accessing collection: '{COLLECTION_NAME}'")
        
        # Count the number of documents in the collection
        document_count = collection.count_documents({})
        
        print("-" * 30)
        print(f"SUCCESS: The collection contains {document_count} documents.")
        print("-" * 30)

    except pymongo.errors.ConnectionFailure as e:
        print(f"ERROR: Could not connect to MongoDB. Please ensure the Docker container is running.")
        print(f"Error details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if client:
            client.close()
            print("Connection to MongoDB closed.")

if __name__ == "__main__":
    check_database()