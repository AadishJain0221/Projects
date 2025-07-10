import oracledb
from oracle_db import connect_oracle_db
from note import Note
 
class Contact:
    def __init__ (self,name,phone,email,contact_id=None):
        self.id=contact_id
        self.name=name
        self.phone=phone
        self.email=email

    def save(self):
        conn=connect_oracle_db()

        if conn is None:
            print("Database connection failed. Cannot save contact.")
            return
        
        try:
            cursor=conn.cursor()

            if self.id is None:
                SQL="INSERT INTO CONTACTS (NAME, PHONE, EMAIL) VALUES (:1, :2, :3) RETURNING ID INTO :4"
                id_var= cursor.var(oracledb.NUMBER)
                cursor.execute(SQL, (self.name, self.phone, self.email, id_var))
                self.id=id_var.getvalue()[0]
                print(f"Contact '{self.name}' added with ID: {self.id}")
            else:
                SQL="UPDATE CONTACTS SET NAME=:1, PHONE=:2, EMAIL=:3 WHERE ID=:4"
                cursor.execute(SQL, (self.name, self.phone, self.email, self.id))
                print(f"Contact ID {self.id} updated")

            conn.commit()

        except oracledb.Error as e:
            error_obj,=e.args
            print(f"Error saving contact : {error_obj.message}")
            conn.rollback()
        
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    @classmethod    
    def getall(cls):
        print("debug: contact.getall before connection")
        conn=connect_oracle_db()

        if conn is None:
            print("Cannot retrieve contacts : Oracle database connection failed.")
            return []
        
        print("debug: contact.getall after connection")
        contacts=[]
        cursor=None
        try:
            cursor=conn.cursor()
            SQL="SELECT ID, NAME, PHONE, EMAIL FROM CONTACTS ORDER BY NAME"
            cursor.execute(SQL)
            rows=cursor.fetchall()
            for row in rows:
                contacts.append(cls(contact_id=row[0], name=row[1], phone=row[2], email=row[3]))

        except oracledb.Error as e:
            error_obj,=e.args
            print(f"Error retrieving contacts: {error_obj.message}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return contacts

    @classmethod
    def get_by_id(cls, contact_id):

        conn=connect_oracle_db()
        if conn is None:
            print("Cannot retrieve contact: Oracle database connection failed.")
            return None
        
        contact=None
        cursor=None

        try:
            cursor=conn.cursor()
            SQL="SELECT ID, NAME, PHONE, EMAIL FROM CONTACTS WHERE ID=:1"
            cursor.execute(SQL ,(contact_id,))#Pass ID as a tuple
            row= cursor.fetchone()# Fetches single result
            if row:
                contact=cls(contact_id=row[0], name=row[1], phone=row[2], email=row[3])

        except oracledb.Error as e:
            error_obj,=e.args
            print(f"Error retrieving contacts: {error_obj.message}")
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return contact
    
    def delete(self):
        if self.id is None:
            print("Contact cannot be deleted: No ID provided.")
            return False

        conn=connect_oracle_db()
        if conn is None:
            print("Cannot delete contact: Oracle database connection failed.")
            return False
        
        cursor=None

        try:
            cursor=conn.cursor()    
            SQL="DELETE FROM CONTACTS WHERE ID=:1"
            cursor.execute(SQL,(self.id,))
            conn.commit()
            print("Contact deleted successfully from Oracle with ID:",self.id)

            # Cascade delete notes for this contact
            Note.delete_all_for_contact(self.id)# calls the delete all note methode from notes.py
            return True
        
        except oracledb.Error as e:
            error_obj,=e.args
            print(f"Error deleting contact ID {self.id}: {error_obj.message}")
            conn.rollback() # to rollback if delete fails
            return False
        
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        

            