from dotenv import load_dotenv  # import load_dotenv to load environment variables from a .env file

import os

from fastapi.responses import JSONResponse  # import JSONResponse to return JSON responses

from fastapi import FastAPI,HTTPException, Path,Query,Depends,Request  
from service.products import (get_all_products,
                            add_product,
                            remove_product,
                            change_product,
                            load_products
                            )  # import service functions for products
from schema.product import Product, ProductUpdate  # import Pydantic models for product validation
from uuid import uuid4,UUID  # import uuid4 to generate unique identifiers
from datetime import datetime  # import datetime for timestamping
from typing import List  # import List for type annotations


load_dotenv()  # load environment variables from the .env file

app=FastAPI()  # to create an instance of FastAPI class


'''koi bhi http request aane se pehle aur response jane se 
pehle ye middleware run hoga 
'''

# @app.middleware("https")
# async def lifecycle(request:Request,call_next):
#     print("B>>>efore request")
#     response=await call_next(request)
#     print("During request")
#     response=await call_next(request)
#     print("After request")
#     return response


'''its a staitic route mens kitni baar bhi same route call hoga
to same response milega'''


'''Depndency Injection ka use karte hai to hum ek function ko
dusre function me as a parameter pass karte hai and usko reuse karte hai
'''
def common_logic():
    print ("This is a common logic that can be reused in multiple routes")



@app.get('/',response_model=dict)  # decorator to define a route for the root endpoint 
def root(deps=Depends(common_logic)):  # use dependency injection to include common logic
    DB_PATH=os.getenv("BASE_URL")  # get the database path from environment variables

    # return {"message": "Hello World","data_path":DB_PATH}  # return a JSON response with a message

    return JSONResponse(
        status_code=200,
        content={"message": "Hello World",
                "dependency": deps,
                "data_path":DB_PATH},
    )

# dynamic route with a path parameter 'id'
# @app.get("/products/{id}") 
# def get_products(id:int):  # 'id' is expected to be an integer
    products=["laptop","mobile","tablet"]  # list of products

    return products[id]  if products[id] else HTTPException(status_code=404,detail="Product not found")  # return the product at index 'id' or raise an HTTPException if not found

''' reponse_model ye btata hai return hone wale data ka structure
kya hoga aur usko validate bhi karta hai
'''


@app.get("/products",response_model=List[Product])  # define a route to get all products with a response model of a list of Product
def get_products():
    return get_all_products()  # call the service function to get all products and return the result



# Query Parameter 
@app.get("/products")
def list_products(
    dep=Depends(load_products),  # use dependency injection to include common logic
    name:str=Query(
    default=None,
    min_length=1,
    max_length=50,
    description="Search by product name(case insensitive)",
    examples=["laptop"]
    ),

    # Sorting and Ordering Query Parameters
    sort_by_price:bool=Query(
        default=False,
        description="Sort products by price"
    ),
    order: str=Query(default="asc",description="Order of sorting: 'asc' for ascending, 'desc' for descending"),


    limit:int=Query(
        default=10,
        ge=1, # greater than or equal to 1
        le=100, # less than or equal to 100
        description="Number of items to return"
    ),

    offset:int=Query(
        default=0,
        ge=0, # greater than or equal to 0
        description="Paginination offset"
    )

):  # define a query parameter 'name' with validation

    # products=get_all_products()  # call the service function to get all products

    products=dep  # use the dependency-injected function to get all products

    if name:
        needle=name.strip().lower()  # normalize the search term
        products=[p for p in products if needle in p.get("name","").lower()]

    if not products:
        raise HTTPException(status_code=404,detail=f"No products found with name ={name}")  # raise an exception if no products match the search term

    if sort_by_price:
        reverse=order=="desc"  # determine the sorting order based on the 'order' query parameter

        products=sorted(products,key=lambda p:p.get("price",0),reverse=reverse)  # sort the products by price in the specified order

    total=len(products)  # get the total number of matching products

    products=products[offset:offset+limit]  # limit the number of products returned based on the 'limit' query parameter 

    return {"total":total,"items":products}  # return a JSON response with the total count and the list of matching products


# For any value it will run for 
'''To validation ke liye hum ishme Path lagayenge'''
@app.get("/products/{product_id}")
def get_product_by_id(
    product_id: UUID = Path(
        ...,
        description="UUID of the product",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
):
    products=get_all_products()

    for product in products:
        if product["id"] == str(product_id):
            return product

    raise HTTPException(status_code=404,detail="Product not found")

'''Jab hamare POST me request bhejte hai to data hame data ko
validate karna padta hai aur uske liye ham Pydantic ka use 
karte hai and hme kyuki data structured way me chahiye hota hai 
ish liye hum usko dictonary me mangte hai
'''


# @app.post("/products",status_code=201)
# def create_product(product:Product):
#     return product.model_dump(mode="json")  # return the validated product data as a dictionary


''' newly added chijo ko bs json ke form just dump kr diya hai'''



@ app.post("/products",status_code=201)
def create_product(product:Product):
    product_dict=product.model_dump(mode="json")  # convert the Pydantic model to a dictionary
    product_dict["id"]=str(uuid4()) # generate a new UUID for the product
    product_dict["created_at"]=datetime.utcnow().isoformat()+"Z" # add the current timestamp in ISO format

    try:
        add_product(product_dict)  # call the service function to add the new product
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))  # raise an HTTPException if the product already exists
    


    return product.model_dump(mode="json")  # return the product data with the new UUID and timestamp



@app.delete("/products/{product_id}")
def delete_product(product_id: UUID=Path(
    ...,
    description="UUID of the product to delete"
)):
    try:
        res=remove_product(str(product_id))  # call the service function to remove the product by ID
        return res

    except ValueError as e:
        raise HTTPException(status_code=404,detail=str(e))  # raise an HTTPException if the product is not found


@app.put("/products/{product_id}")
def update_product(
    product_id: UUID=Path(
        ...,
        description="UUID of the product to update",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    ),
    payload: ProductUpdate=...,
):
    try:
        updated_product=change_product(
            str(product_id),
            payload.model_dump(mode="json",exclude_unset=True)
        )
        return updated_product

    except ValueError as e:
        raise HTTPException(status_code=404,detail=str(e))  # raise an HTTPException if the product is not found