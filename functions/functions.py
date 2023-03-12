import random
import string
from datetime import datetime
import os
from db.database import add_product,get_files,update_file,find_file
import base64
import json

def create_user_folder(user_id):
    # Create a directory for the user in the Uploads/USERID/profile folder
    folder_path = os.path.join("Uploads", user_id, "profile")
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def generate_order_id():
    # Generate a 10-digit alphanumeric string with "ORDERID" appended
    return "O_" + "".join(random.choices(string.ascii_uppercase + string.digits, k=10))


def generate_user_id():
    # Generate a 6-digit alphanumeric string with "USERID" appended
    return "U_" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

def create_new_order(order: dict):
    # validate inputs
    if not order.__getattribute__('product_details'):
        raise ValueError("Product details is required")
    product_details = order.__getattribute__('product_details')
    for product in product_details:
        if not product.__getattribute__('product_name'):
            raise ValueError("Product name is required")
        if not product.__getattribute__('price') or product.__getattribute__('price') <= 0:
            raise ValueError("Price must be a positive number")
        if not product.__getattribute__('quantity') or product.__getattribute__('quantity') <= 0:
            raise ValueError("Quantity must be a positive number")
        product_img = product.__getattribute__('product_img')

        if not product_img or not product_img["filename"].lower().endswith(('.jpg', '.jpeg', '.png')):
            raise ValueError("Invalid product image file")
    if not order.__getattribute__("status"):
          raise ValueError("status is empty")

    # generate new order and user IDs
    order_id = generate_order_id()
    user_id = generate_user_id() if order.__getattribute__("user_id")=="" or not order.__getattribute__("user_id") else order.__getattribute__("user_id")

    # save product images to local folder
    upload_folder = create_user_folder(user_id=user_id)
    products = []
    for product in product_details:
        img_string = product.__getattribute__('product_img')["data"]
        img_data = base64.b64decode(img_string)
        filename = f"{product.__getattribute__('product_img')['filename']}"
        with open(os.path.join(upload_folder, filename), 'wb') as f:
            f.write(img_data)
    for product in product_details:
        jsonstring = json.dumps(product.__dict__)
        products.append(json.loads(jsonstring))
    

    # insert new order to MongoDB
    new_order = {
        'order_id': order_id,
        'user_id': user_id,
        'product_details': products,
        'status': order.__getattribute__('status'),
        'order_date_time': datetime.now(),
    }
    result = add_product(new_order)
    return result

def get_allorders():
    try: 
        files = get_files()
        for file in files:
            amount = 0
            for product in file['product_details']:
                amount += product['price']
            file['total_amount'] = amount
        return files
    except Exception as e:
        return f"Error while fetching details: {e}"

def update_orders(orders):
    try: 
        ans = []
        for order in orders:
            query = {'order_id':order["order_id"],'user_id':order["user_id"]}
            update = {'updated_order_date_time':order["updated_order_date_time"],'status':order["status"]}
            update_file(query=query,update=update)
            if(order["status"].lower()=="confirmed"):
                file= find_file(order_id=order["order_id"],user_id=order["user_id"])
                result = {
                    'order_id': file['order_id'],
                }
                product_details=[]
                total_amount = 0
                for product in file['product_details']:
                    temp = {
                        'product_name':product['product_name'],
                        'price':product['price'],
                        'quantity':product['quantity']
                    }
                    total_amount+=product['price']
                    product_details.append(temp)
                result['product_details'] = product_details
                result['total_amount'] = total_amount
                ans.append(result)
        return ans
    except Exception as e:
        return f'Error while updating order: {e}'
                
