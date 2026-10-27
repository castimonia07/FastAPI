from pydantic import (
    AnyUrl, BaseModel, 
    Field,field_validator,
    model_validator,computed_field,
    EmailStr
    )  # import BaseModel from Pydantic for data validation
from typing import Annotated, List, Optional  # import typing utilities for type annotations
from uuid import UUID  # import UUID for unique identifier validation
from datetime import datetime



from pydantic import BaseModel


class Seller(BaseModel):
  id: UUID
  name: Annotated[
    str,
    Field(
      min_length=2,
      max_length=60,
      title="Seller Name",
      description="Name of the seller",
      example="John's Electronics",
    ),
  ]
  email:EmailStr
  website:AnyUrl


  @field_validator("email",mode="after")
  @classmethod
  def validate_seller_email_domain(cls,value:EmailStr):
    allowed_domains=["mistore.in","hpworld.in"]

    domain=str(value).split("@")[-1].lower()
    if domain not in allowed_domains:
        raise ValueError(f"Email domain must be one of {allowed_domains}")

    return value




class Dimensions(BaseModel):
  length: Annotated[float,Field(
    default=0.0,
    title="Length in cm",
    description="Length of the product in centimeters",
    ge=0.0,
    example=30.5,
  )]
  width: Annotated[float,Field(
    default=0.0,
    title="Width in cm",
    description="Width of the product in centimeters",
    ge=0.0,
    example=20.0,
  )]
  height: Annotated[float,Field(
    default=0.0,
    title="Height in cm",
    description="Height of the product in centimeters",
    ge=0.0,
    example=10.0,
  )]




class Product(BaseModel):
  id: UUID
  sku: Annotated[
    str,  # jo bhi data type yaha mentioned hai whi same datatyoe example me bhi mention krna hai 
    Field(
      min_length=6,
      title="SKU",
      description="Stock Keeping Unit",
      example="241-242-432",
    ),
  ]
  name: str
  description: Annotated[
    Optional[str],
    Field(
      None,
      title="Product Description",
      description="A brief description of the product",
      example="A high-quality laptop with 16GB RAM and 512GB SSD.",
    ),
  ]
  tags: Annotated[
    Optional[list[str]],
    Field(
        None,   
        max_length=10,
        title="Product Tags",
        description="A list of tags associated with the product",
        example=["electronics", "laptop", "gaming"],
    )
  ]
  rating: Optional[float] = Field(
    default=None,
    title="Product Rating",
    description="Average rating of the product (0.0 to 5.0)",
    ge=0.0,
    le=5.0,
    example=4.5,
    )
  
  image_urls: Annotated[
    List[AnyUrl],
    Field(
        default=[],
        title="Product Image URLs",
        description="A list of URLs pointing to images of the product",
        example=["https://example.com/image1.jpg", "https://example.com/image2.jpg"],
    )
  ]
  discount_percent: Annotated[
    Optional [float],
    Field(
        default=0.0,
        title="Discount Percentage",
        description="Discount percentage for the product (0.0 to 100.0)",
        ge=0.0,
        le=100.0,
        example=10.0,
    )
  ]

  stock: Annotated[
    int,
    Field(
        default=0,
        title="Stock Quantity",
        description="Number of items available in stock",
        ge=0,
        example=50,
    )
  ]

  is_active: Annotated[
    bool,
    Field(
        default=True,
        title="Is Active",
        description="Indicates whether the product is active and available for purchase",
        example=True,
    )
  ]

  price: Annotated[
    float,
    Field(
        default=0.0,
        title="Product Price",
        description="Price of the product in USD",
        ge=0.0,
        example=999.99,
    )
  ]
  


  dimension_cm:Dimensions

  seller:Seller

  created_at: datetime


  @field_validator("sku",mode="after") # mode="after" means after the value is assigned to the field, this validator will be called
  @classmethod
  def validate_sku_format(cls,value:str):
    if "-" not in value:
      raise ValueError("SKU must contain a '-'")

    last=value.split("-")[-1]
    if not (len(last)==3 and last.isdigit()):
      raise ValueError("SKU must end with a 3-digit number after '-'")

    return value


  @model_validator(mode="after")
  @classmethod
  def validate_business_rules(cls,model:"Product"):
    if model.stock==0 and model.is_active is True:
      raise ValueError("Active product cannot have zero stock")
    
    if model.discount_percent>0 and model.rating==0:
      raise ValueError("Discounted product cannot have zero rating")

    return model

  @computed_field
  @property
  def final_price(self)->float:
    return round(self.price *(1-self.discount_percent/100),2)


  @computed_field
  @property
  def volume_cm3(self)->float:
    d=self.dimension_cm
    return round(d.length*d.width*d.height,2)






''' field validator keval ek field pe kaam krta hai like
sku me hme check krna hai koi condition to ye use kr skte hai
for multiple field validation hme model_validator ka use karna padta hai
'''





#  For UPDATE OPERATION 


class Seller(BaseModel):
    id: Optional[UUID] = None

    name: Optional[Annotated[
        str,
        Field(
            min_length=2,
            max_length=60,
            title="Seller Name",
            description="Name of the seller",
            example="John's Electronics",
        ),
    ]] = None

    email: Optional[EmailStr] = None
    website: Optional[AnyUrl] = None

    @field_validator("email", mode="after")
    @classmethod
    def validate_seller_email_domain(cls, value):
        if value is None:
            return value

        allowed_domains = ["mistore.in", "hpworld.in"]

        domain = str(value).split("@")[-1].lower()

        if domain not in allowed_domains:
            raise ValueError(
                f"Email domain must be one of {allowed_domains}"
            )

        return value


class Dimensions(BaseModel):
    length: Optional[float] = Field(
        default=None,
        title="Length in cm",
        description="Length of the product in centimeters",
        ge=0.0,
        example=30.5,
    )

    width: Optional[float] = Field(
        default=None,
        title="Width in cm",
        description="Width of the product in centimeters",
        ge=0.0,
        example=20.0,
    )

    height: Optional[float] = Field(
        default=None,
        title="Height in cm",
        description="Height of the product in centimeters",
        ge=0.0,
        example=10.0,
    )


class ProductUpdate(BaseModel):
    id: Optional[UUID] = None

    sku: Optional[
        Annotated[
            str,
            Field(
                min_length=6,
                title="SKU",
                description="Stock Keeping Unit",
                example="241-242-432",
            ),
        ]
    ] = None

    name: Optional[str] = None

    description: Optional[
        Annotated[
            str,
            Field(
                title="Product Description",
                description="A brief description of the product",
                example="A high-quality laptop with 16GB RAM and 512GB SSD.",
            ),
        ]
    ] = None

    tags: Optional[
        Annotated[
            list[str],
            Field(
                max_length=10,
                title="Product Tags",
                description="A list of tags associated with the product",
                example=["electronics", "laptop", "gaming"],
            ),
        ]
    ] = None

    rating: Optional[float] = Field(
        default=None,
        title="Product Rating",
        description="Average rating of the product (0.0 to 5.0)",
        ge=0.0,
        le=5.0,
        example=4.5,
    )

    image_urls: Optional[
        Annotated[
            List[AnyUrl],
            Field(
                title="Product Image URLs",
                description="A list of URLs pointing to images of the product",
                example=[
                    "https://example.com/image1.jpg",
                    "https://example.com/image2.jpg",
                ],
            ),
        ]
    ] = None

    discount_percent: Optional[float] = Field(
        default=None,
        title="Discount Percentage",
        description="Discount percentage for the product (0.0 to 100.0)",
        ge=0.0,
        le=100.0,
        example=10.0,
    )

    stock: Optional[int] = Field(
        default=None,
        title="Stock Quantity",
        description="Number of items available in stock",
        ge=0,
        example=50,
    )

    is_active: Optional[bool] = Field(
        default=None,
        title="Is Active",
        description="Indicates whether the product is active and available for purchase",
        example=True,
    )

    price: Optional[float] = Field(
        default=None,
        title="Product Price",
        description="Price of the product in USD",
        ge=0.0,
        example=999.99,
    )

    dimension_cm: Optional[Dimensions] = None

    seller: Optional[Seller] = None

    created_at: Optional[datetime] = None