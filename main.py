from pymongo import errors
from db_connection import db_connect
#30984 Cagri Can Saracaydin
# create a collection in the database
def create_collection(db, collection_name):
    try:
        db.create_collection(collection_name)
        print(f"Collection '{collection_name}' created successfully.")
    except errors.CollectionInvalid:
        print(f"Collection '{collection_name}' already exists.")
    except errors.PyMongoError as e:
        print(f"An error occurred: {e}")

def insert_data(db, collection_name, data):
    try:
        # get the collection
        collection = db[collection_name]
        # insert
        collection.insert_one(data)
        print("Data inserted successfully.")
    except errors.PyMongoError as e:
        print(f"An error occurred while inserting data: {e}")

# read all data from a collection
def read_all_data(db, collection_name):
    try:
        collection = db[collection_name]
        # find all documents in the collection
        data = collection.find()
        data_found = False
        for doc in data:
            print(doc)
            data_found = True
        if not data_found:
            print("No data found in the collection.")
    except errors.PyMongoError as e:
        print(f"An error occurred while reading data: {e}")

#  read data from a collection based on filter criteria
def read_filtered_data(db, collection_name, filter_criteria):
    try:
        collection = db[collection_name]
        # find documents with filter criteria
        data = collection.find(filter_criteria)
        data_found = False
        for doc in data:
            print(doc)
            data_found = True
        if not data_found:
            print("No matching data found.")
    except errors.PyMongoError as e:
        print(f"An error occurred while reading filtered data: {e}")

# check if a document exists in a collection based on filter criteria
def document_exists(collection, filter_criteria):
    return collection.find_one(filter_criteria) is not None

#  update data in a collection
def update_data(db, collection_name, filter_criteria, new_data):
    try:
        collection = db[collection_name]
        # Check if document exists
        if document_exists(collection, filter_criteria):
            # Update the document
            result = collection.update_one(filter_criteria, {"$set": new_data})
            if result.matched_count > 0:
                print("Data updated successfully.")
            else:
                print("No matching document found.")
        else:
            print("No matching document found.")
    except errors.PyMongoError as e:
        print(f"An error occurred while updating data: {e}")

# delete data from a collection
def delete_data(db, collection_name, filter_criteria):
    try:
        collection = db[collection_name]
        # Delete the document
        result = collection.delete_one(filter_criteria)
        if result.deleted_count > 0:
            print("Data deleted successfully.")
        else:
            print("No matching document found.")
    except errors.PyMongoError as e:
        print(f"An error occurred while deleting data: {e}")

# get user input with optional validation
def get_user_input(prompt, validation_func=None):
    while True:
        value = input(prompt)
        if validation_func:
            if validation_func(value):
                return value
            else:
                print("Invalid input. Please try again.")
        else:
            return value

# display the main menu and get user's choice
def main_menu():
    print("\nWelcome to the Financial Management Portal!")
    print("Please pick the option that you want to proceed.")
    print("1 - Create a collection.")
    print("2 - Read all data in a collection.")
    print("3 - Read some part of the data while filtering.")
    print("4 - Insert data.")
    print("5 - Delete data.")
    print("6 - Update data.")
    print("0 - Exit.")
    return get_user_input("Selected option: ", lambda x: x.isdigit() and 0 <= int(x) <= 6)

# display the collection menu and get user's choice
def collection_menu(db):
    collections = db.list_collection_names()
    if not collections:
        print("No collections found. Please create a collection first.")
        return None

    print("\nPlease select the collection:")
    for i, collection in enumerate(collections, start=1):
        print(f"{i} - {collection}")

    while True:
        selected_option = get_user_input("Selected option: ")
        if selected_option.isdigit() and 1 <= int(selected_option) <= len(collections):
            return collections[int(selected_option) - 1]
        else:
            print("Invalid selection. Please try again.")


# get the collection name based on user's choice
def get_collection_name(option):
    return "FinancialGoals" if option == '1' else "Budgets"

def main():
    # Connect to the database
    db = db_connect()
    if db is None:
        print("Unable to connect to the database. Please check your connection settings.")
        return

    while True:
        # display the main menu and get user input
        option = main_menu()
        if option == '0':
            break

        # options that require a collection selection
        if option in {'2', '3', '4', '5', '6'}:
            collection_name = collection_menu(db)
            if not collection_name:
                continue

        # perform operations
        if option == '1':
            collection_name = get_user_input("Enter the name of the collection to create: ")
            create_collection(db, collection_name)
        elif option == '2':
            read_all_data(db, collection_name)
        elif option == '3':
            field = get_user_input("Enter the field to filter by: ")
            value = get_user_input("Enter the value to filter by: ")
            read_filtered_data(db, collection_name, {field: value})
        elif option == '4':
            data = {}
            print("Enter the data fields (key:value pairs). Type 'done' when finished.")
            while True:
                field = get_user_input("Field: ")
                if field.lower() == 'done':
                    break
                value = get_user_input("Value: ")
                data[field] = value
            insert_data(db, collection_name, data)
        elif option == '5':
            field = get_user_input("Enter the field to filter by: ")
            value = get_user_input("Enter the value to filter by: ")
            delete_data(db, collection_name, {field: value})
        elif option == '6':
            print("Enter the criteria to identify the document to update.")
            filter_field1 = get_user_input("Filter field 1: ")
            filter_value1 = get_user_input(f"Value for {filter_field1}: ")
            filter_field2 = get_user_input("Filter field 2: ")
            filter_value2 = get_user_input(f"Value for {filter_field2}: ")

            print("Enter the new data to update.")
            new_field = get_user_input("Field to update: ")
            new_value = get_user_input("New value: ")

            filter_criteria = {filter_field1: filter_value1, filter_field2: filter_value2}
            new_data = {new_field: new_value}

            update_data(db, collection_name, filter_criteria, new_data)

if __name__ == "__main__":
    main()
