import pymongo

from pymongo import MongoClient


uri = "mongodb://localhost:27017/"
client = MongoClient(uri)

db = client.contacts_db #database creation 
collection  = db.contacts #collection creation


def add_contact(name,email,phone):
    contact={"name":name,"email":email,"phone":phone}
    result = collection.insert_one(contact)
    print(f"contact added with Inserted_ID:{result.inserted_id}")

def show_contact():
    print("\n ___Contact Lists___")
   # print(collection.find())
    for contact in collection.find():
        print(f"Name:{contact['name']},Email:{contact['email']},Phone:{contact['phone']}")   

def update_contact(name,new_email=None,new_phone=None):
    updates={} #new document

    if new_email:
        updates["email"]=new_email
    if new_phone:
        updates["phone"] = new_phone

    result = collection.update_one({"name":name},{"$set":updates})   
    print(f"Updated {result.modified_count} Contact(s)")        


def delete_contact(name):
    result = collection.delete_one({"name":name})  
    print(f"Deleted {result.deleted_count} Contact(s)") 

def Menu():
    while True:
        print("\n1.Add contact")
        print("2.Show contact")
        print("3.Update contact")
        print("4.Delete Contact")
        print("5.Exit")


        choice = input("Enter your choice: ")

        if(choice == '1'):
            name = input("name: ")
            email = input("email: ")
            phone = input("phone: ")
            add_contact(name,email,phone)

        elif(choice == '2'):
            show_contact()

        elif(choice=='3'):
            name = input("Enter name to update: ")
            email = input("Enter email or leave blanck: ")
            phone = input("ENter phone or leave blank: ")

            update_contact(name,new_email=email if email else None,new_phone=phone if phone else None)


        elif(choice=='4'):
            name = input("Enter a name to Delte: ")
            delete_contact(name)


        elif(choice=='5'):
            break      
        
        else:
            print("Enter a valid choice")

Menu()