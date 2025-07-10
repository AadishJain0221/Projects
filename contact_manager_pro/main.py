import os
import time # for time.sleep for better user experience
from dotenv import load_dotenv

#import our database connection and model classes
from oracle_db import init_oracle_db
from mongo_db import check_mongo_connection
from contact import Contact
from note import Note

#load environment variables
load_dotenv()

def clear_screen():
    # to clear terminal screen
    os.system('cls' if os.name=='nt' else 'clear')

def display_menu():
    print("\n----- MENU -----")
    print("1. Add New Contact")
    print("2. View All Contact")
    print("3. View Contact Details & Notes")
    print("4. Update Contact")
    print("5. Delete Contact")
    print("6. Add Note to Contact")
    print("7. Delete Note")
    print("8. Exit")
    print("----------------")

def get_integer_input(prompt):
    # to get a valid integer input
    while True:
        try:
            value=int(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a correct number")


def add_contact():
    # for adding and saving new contact details
    print("\n--- Add New Contact ---")
    name=input("Enter contact name:").strip()
    phone=input("Enter phone number (optional)").strip()
    email=input("Enter email address (optional)").strip()

    if not name:
        print("Error: Contact name cannot be empty.")
        time.sleep(2)
        return
    
    contact=Contact(name=name,phone=phone,email=email)
    contact.save()
    time.sleep(2)

def view_all_contact():
    # to retrieve and display all contacts from the database
    print("\n--- All Contacts ---")
    contacts=Contact.getall()

    if not contacts:
        print("No contacts found.")
        return
    else:
        print(f"{'ID':<5} {'Name':<25} {'Phone':<20} {'Email':<30}")
        print("-"*80)
        for contact in contacts:
            print(f"{contact.id:<5} {contact.name:<25} {contact.phone:<20} {contact.email:<30}")
        time.sleep(3)

def view_contact_details():
    # To retrieve and display details associated with the given contact ID
    print("\n--- View Contact Details & Notes ---")
    contact_id=get_integer_input("Enter Contact ID: ")
    contact=Contact.get_by_id(contact_id)

    
    if contact is None:
        print(f"Contact with ID: {contact_id} not found.")
        time.sleep(2)
        return
    
    print(f"\n--- Details for Contact ID: {contact_id} ---")
    print(f"Name: {contact.name}")
    print(f"Phone: {contact.phone if contact.phone else 'N/A'}")
    print(f"Email: {contact.email if contact.email else 'N/A'}")

    print("\n--- Associated Notes ---")
    notes =Note.get_contact_by_contact_id(contact.id)
    if not notes:
        print("No notes for this contact.")
    else:
        for i, note in enumerate(notes):
            content_display =note.content[:50] +"..." if len(note.content)>50 else note.content 
            print(f"{i+1}. ID: {note.id} | Content: {content_display} | Time: {note.timestamp.strftime('%y-%m-%d %H:%M')}")
        time.sleep(3)

def update_contact():
    # Inputs contact Id and new details to update an existing contact
    print("\n--- Update Contact ---")
    contact_id=get_integer_input("Enter Contact ID to update:")

    contact=Contact.get_by_id(contact_id)
    if contact is None:
        print(f"Contact with ID {contact_id} not found.")
        time.sleep(2)
        return
    
    print(f"Current details for ID {contact.id}: Name='{contact.name}', Phone='{contact.phone}', Email='{contact.email}' ")
    print("Enter new details (leave blank to keep the current value):")

    new_name=input(f"New Name ({contact.name}):").strip()
    new_phone=input(f"New Phone ({contact.phone}):").strip()
    new_email=input(f"New Email ({contact.email}):").strip()

    if new_name:
        contact.name= new_name
    if new_phone:
        contact.phone= new_phone
    if new_email:
        contact.email=new_email

    contact.save()
    time.sleep(2)

def delete_contact():
    # Prompts for a contact ID and deletes the contaxt and its notes.
    print("\n--- Delete Contact ---")
    contact_id=get_integer_input("Enter Contact ID to Delete:")
    
    contact=Contact.get_by_id(contact_id)
    if contact is None:
        print(f"Contact with ID {contact_id} not found.")
        time.sleep(2)
        return
    
    confirm= input(f"Are you sure you want to delete contact '{contact.name}' (ID: {contact.id}) and all its notes? (yes/no): ").strip().lower()
    if confirm =='yes' :
        if contact.delete():# This will also trigger note deletion
            print(f"Contact {contact.id} and associated notes successfully deleted.")
        else:
            print(f"Failed to delete contact { contact.id}")
    else:
        print("Contact deletion cancelled")
    time.sleep(2)

def add_note_to_contact():
    # Prompts foe contact ID and adds a new note.
    print("\n--- Add Note to Contact ---")
    contact_id= get_integer_input("Enter Contact ID to add a note to: ")

    # Check if contact exists first
    contact=Contact.get_by_id(contact_id)
    if contact is None:
        print(f"Contact with ID {contact_id} not found. Cannot add note.")
        time.sleep(2)
        return
    
    content= input("Enter note content: ").strip()
    if not content:
        print("Note content cannot be empty.")
        time.sleep(2)
        return
    
    note=Note(contact_id=contact_id, content=content)
    note.save()
    time.sleep(2)

def delete_note():
    # Prompts for note ID and deletes it.
    print("\n--- Delete Note ---")
    note_id= get_integer_input("Enter Note ID to delete: ")

    if Note.delete_by_id(note_id):
        print(f"Note {note_id} successfully deleted.")
    else:
        print(f"Failed to delete note {note_id}")
    time.sleep(2)

def main():
    # Main Function to run the contact and notes manager application. 
    clear_screen()
    print("Initializing databases...")

    init_oracle_db()
    mongo_connected = check_mongo_connection()

    if not mongo_connected:
        print("\nWarning: MongoDB is not connected. Notes functionality will not work.")
        print(" Please ensure your MongoDB erver is running And MONGODB_URI/MONGODB_NAME are correct in .env.")
        time.sleep(5)

    while True:
        clear_screen()
        display_menu()
        choice= input(" Enter your choice: ").strip()

        match choice:
            case '1':
                add_contact()
            case '2':
                view_all_contact()
            case '3':
                view_contact_details()
            case '4':
                update_contact()
            case '5':
                delete_contact()
            case '6':
                if mongo_connected:
                    add_note_to_contact()
                else:
                    print("MongoDB is not connected. Cannot add notes.")
                    time.sleep(2)
            case '7':
                if mongo_connected:
                    delete_note()
                else:
                    print("MongoDB is not connected. Cannot add notes.")
                    time.sleep(2)
            case '8':
                print("Exiting application. Goodbye!")
                break
            
            case _:
                print("Invalid choice. Please enter a number between 1 and 8.")
                time.sleep(2)

        if choice!='8':
            input("\nPress Enter to continue...")

if __name__=="__main__":
    main()