import pymongo


def initiate_db():
    try:

        # connect to MongoDB
        client = pymongo.MongoClient(
            "mongodb+srv://shopping:shopping@cluster0.xr0djju.mongodb.net/?retryWrites=true&w=majority")

        db = client["product"]
        collection = db["product_details"]
        return client, collection

    except pymongo.errors.ConnectionFailure as e:
        print("Error connecting to MongoDB:", e)
        return None, None


def close_client(client):
    try:
        # close the client connection
        client.close()

    except Exception as e:
        print("Error closing MongoDB client:", e)


def add_product(pd):
    try:
        client, collection = initiate_db()
        print("from here",pd)
        # insert given product details to the db
        result = collection.insert_one(pd)

        return f"Product Details added successfully with ID: {result.inserted_id}"

    except Exception as e:
        return f"Error adding product: {e}"
    finally:
        close_client(client)


def find_file(order_id,user_id):
    try:
        client, collection = initiate_db()

        # search for file with given order ID
        file = collection.find_one({
            "order_id": order_id,"user_id":user_id})
        # close MongoDB client connection
        
        return file
    
    except Exception as e:
        print("Error getting product details:", e)

    finally:
        close_client(client)

def get_files():
    try:
        client, collection = initiate_db()

        # search for file with given order ID
        file = list(collection.find())
        # close MongoDB client connection

        return file
    
    except Exception as e:
        return f"Error getting product details: {e}"

    finally:
        close_client(client)


def update_file(query, update):
    try:
        client, collection = initiate_db()
        # update the documents that match the query
        result = collection.update_many(query,{'$set':  update})
        return f"Updated  {result.modified_count} documents"

    except Exception as e:
        return f"Error updating data: {e}"

    finally:
        close_client(client)
