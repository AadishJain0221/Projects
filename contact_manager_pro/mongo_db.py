import os 
from pymongo import MongoClient
from dotenv import load_dotenv
from pymongo.errors import PyMongoError

load_dotenv()

def get_mongo_collection(collection_name):

    mongo_uri=os.getenv('MONGODB_URI')
    mongo_db_name=os.getenv('MONGODB_DB_NAME')

    if not mongo_uri or not mongo_db_name:
        print("MongoDB URI or DB Name not found in environment variables.")
        return None
    
    try :
        client= MongoClient(mongo_uri)
        db=client[mongo_db_name]
        collection=db[collection_name]
        return collection
    
    except Exception as e:
        print(f"Error connecting to MongoDB or getting collection '{collection_name}' : {e}")
        return None
    
def check_mongo_connection():
    mongo_uri=os.getenv('MONGODB_URI')

    if not mongo_uri:
        print("MongoDb URI not found in environment variables")
        return False

    try:
        client=MongoClient(mongo_uri, serverselectionTimeoutMS=5000)
        client.admin.command('ping')
        print("Succesfully cnnected to MongoDB.")
        return True
    
    except Exception as e:
        print(f" Failed to connect to MongoDB : {e}")
        return False

def get_next_sequence_value(name):
    # Generates a unique , auto-incrementing integer ID for a given equence name.
    # Uses a 'counters' collection in MongoDB.

    counters_collection= get_mongo_collection('counters')
    if counters_collection is None:
        print("Error: Could not access counters collection. Cannot generate sequence ID.")
        return None
    
    try:
        # Automatically increments the sequence value for the given name
        # upsert=True means it will create the document if it dosen't exist
        sequence_doc=counters_collection.find_one_and_update(
            {'_id':name}
            ,{'$inc': {'sequence_value':1}},
            upsert= True,
            return_document=True #Return the updated document
        )
        print(f"Successfully generated ID: {sequence_doc['sequence_value']}")
        return sequence_doc['sequence_value']
    
    except PyMongoError as e:
        print (f"An unexpected error occurred while generating sequence ID: {e}")
        return None
    except Exception as e:
        print("Unexpected error:",e)
        return None

if __name__=="__main__":
    print("Checking MongoDB connection...")
    if check_mongo_connection():
        notes_coll= get_mongo_collection('Notes')
        if notes_coll is not None:
            print(f"Successfully accessed 'Notes' collection. Count : {notes_coll.count_documents({})}")

        print("\nTesting sequence generator: ")
        next_id= get_next_sequence_value("noteid")
        if next_id is not None:
            print (f"Next Note ID: {next_id}")
            next_id= get_next_sequence_value("noteid")
            print(f"Next Note ID (again): {next_id}")
        else:
            print("Failed to get next sequence ID.")
    else:
        print("MongoDb connection test failed.")