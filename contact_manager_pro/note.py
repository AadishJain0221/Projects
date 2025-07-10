from datetime import datetime
from mongo_db import get_mongo_collection, get_next_sequence_value

class Note:

    def __init__ (self, contact_id , content, note_id=None,timestamp=None):
        self.contact_id=contact_id
        self.content=content 

        if note_id is None:
            generated_id = get_next_sequence_value("noteid")
            if generated_id is None:
                raise Exception("Failed to Generate a unique Note ID.")
            self.id = generated_id
        else:
            try:
                self.id=int(note_id)
            except(ValueError,TypeError) as e:
                raise ValueError(f"Invalid note_id provided for existing note: {note_id}")

        self.timestamp=timestamp if timestamp else datetime.now()

    def save(self):
        notes_collection= get_mongo_collection('notes')

        if notes_collection is None:
            print("Cannot save note: MongoDB connection failed")
            return

        try:
            note_document={
                "_id":self.id ,
                "contact_id":self.contact_id,
                "content":self.content,
                "timestamp":self.timestamp
            }
            notes_collection.insert_one(note_document)
            print("Note added for Contact ID:",self.contact_id, "with Note ID :",self.id)

        except Exception as e:
            print(f"Error saving note: {e}")

    @classmethod
    def get_contact_by_contact_id(cls,contact_id):
        notes_collection= get_mongo_collection('notes')

        if notes_collection is None:
            print("Cannot retrieve note: MongoDB connection failed")
            return

        notes =[]

        try:
            for doc in notes_collection.find({"contact_id": contact_id}).sort("timestamp",1):
                notes.append(cls(
                    contact_id=doc['contact_id'],
                    content=doc['content']
                    ,note_id=doc['_id']
                    ,timestamp=doc['timestamp']
                ))
            
        except Exception as e:
            print(f"Error retrieving notes for contact ID {contact_id} : {e}")
        
        return notes
    
    @classmethod
    def delete_by_id(cls,note_id):
        notes_collection= get_mongo_collection('notes')

        if notes_collection is None:
            print("Cannot delete note: MongoDB connection failed")
            return

        try:
            result = notes_collection.delete_one({"_id": int(note_id)})  
            if result.delete_count>0:
                print(f"Note ID {note_id} deleted from MongoDB.")
                return True
            
            else:
                print(f"Note ID {note_id} not found.")
                return False
            
        except Exception as e:
            print(f"Error deleting note ID {note_id}: {e}")
            return False
        
    @classmethod
    def delete_all_for_contact(cls,contact_id):
        notes_collection= get_mongo_collection('notes')

        if notes_collection is None:
            print("Cannot delete notes for contact: MongoDB connection failed")
            return

        try:
            result = notes_collection.delete_many({"contact_id":contact_id})
            print(f"Deleted {result.deleted_count} notes for Contact ID {contact_id} from MongoDB.")
        
        except Exception as e:
            print(f"Error deleting all notes for contact ID {contact_id}: {e}")
            