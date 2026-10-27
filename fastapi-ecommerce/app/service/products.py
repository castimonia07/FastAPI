import json
from pathlib import Path
from typing import List,Dict

# DATA_FILE=Path(__file__).parent.parent / "data" / "products.json"


DATA_FILE=Path(__file__).parent.parent / "data" / "dummy.json"


# for loading the products from the json file and returning it as a list of dictionaries
def load_products() ->List[Dict]:
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE,"r",encoding="utf-8") as file:
        return json.load(file)

# for getting all products from the json file
def get_all_products() -> List[Dict]:
    return load_products()


# for saving the products to the json file
def save_product(products:List[Dict]) -> None:
    with open(DATA_FILE, "w",encoding="utf-8") as file:
        json.dump(products,file,indent=2,ensure_ascii=False)  # ascii=false ishliye kiya hai taki deta binary ki jgh actual format me save ho

# for adding a new product to the json file
def add_product(product:Dict)->Dict:
    products=get_all_products()

    if any(p["sku"]==product["sku"] for p in products):
        raise ValueError("Product with the same SKU already exists")

    products.append(product)
    save_product(products)
    return product


def remove_product(id:str)->str:
    products=get_all_products()

    for indx,p in enumerate(products):
        if p["id"]==id:
            deleted=products.pop(indx)
            save_product(products)
            return {"Message":"Product deleted successfully","deleted_product":deleted}


def change_product(product_id:str,update_data:dict):
    products=get_all_products()

    for index,product in enumerate(products):

        for key,value in update_data.items():
            if value is None:
                continue

            if isinstance(value,dict) and isinstance(product.get(key),dict):
                product[key].update(value)
            else:
                product[key]=value

        products[index]=product
        save_product(products)

        return product

    raise ValueError("Product with the given ID not found")