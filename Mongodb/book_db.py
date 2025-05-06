import pymongo
from pymongo import MongoClient

uri="mongodb://localhost:27017/"
client = MongoClient(uri)

db=client.book_Db
collection = db.books


def add_book(name,auther,status):
    res = collection.insert_one({"title":name,"author":auther,"status":status})
    print(f"Book inserted with id {res.inserted_id}")

def view_all_book():
    for book in collection.find():
        print(f"{book['title']},{book['author']},{book['status']}")

def update_status(name,new_status):

    res = collection.update_one({"title":name},{"$set":{"status":new_status}})
    print(f"Updated {res.modified_count} Contact(s)")

def delete_book(name):
    res=collection.delete_one({"title":name})
    print(f"Deleted {res.deleted_count} Contact(s)")

def add_multiple_books(book_list):
    res=collection.insert_many(book_list)
    print(f"{len(res.inserted_ids)} books added successfully!")    


def Menu():
    while True:

        print("\n1.Add book")
        print("2.view all book")
        print("3.update status")
        print("4.delete a book")
        print("5.multiple book add: ")
        print("6.Exit")


        choice = input("enter a choice: ")

        if(choice=='1'):
            name = input("name: ")
            auther = input("author: ")
            status=input("status: ")
            add_book(name,auther,status)
        
        elif(choice=='2'):
            view_all_book()

        elif(choice=='3'):
            name=input("Enter a book name to Upadate status: ") 
            status = input("enter new status: ")
            update_status(name,status)

        elif(choice=='4'):
            name=input("Enter a book name to delete: ")
            delete_book(name) 

        elif(choice=='5'):
           n=int(input("Enter how many books you want to enter: "))
           sample_books = []
           for i in range(n):
               title = input("title: ")
               author = input("author: ")
               genre = input("genre: ")
               status = input("status: ")
               book = {"title":title,"author":author,"genre":genre,"status":status}
               sample_books.append(book)
           
           add_multiple_books(sample_books)

        elif(choice=='6'):
            break  

        else:
            print("Enter a valid choice")       




Menu()