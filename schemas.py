"""
Database Schemas for the Pet Harness Store

Each Pydantic model represents a collection in MongoDB.
Collection name is the lowercase of the class name.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class Product(BaseModel):
    """
    Collection: product
    Represents a pet harness product
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in USD")
    species: str = Field(..., description="Target pet species: dog or cat")
    sizes: List[str] = Field(default_factory=list, description="Available sizes e.g., XS,S,M,L,XL")
    image_url: Optional[str] = Field(None, description="Image URL")
    color: Optional[str] = Field(None, description="Primary color")
    rating: Optional[float] = Field(4.8, ge=0, le=5, description="Average rating")
    in_stock: bool = Field(True, description="Whether product is in stock")

class OrderItem(BaseModel):
    product_id: str = Field(..., description="ID of the product")
    title: str = Field(..., description="Product title at time of order")
    price: float = Field(..., ge=0, description="Unit price at time of order")
    size: Optional[str] = Field(None, description="Selected size")
    quantity: int = Field(1, ge=1, description="Quantity ordered")
    image_url: Optional[str] = None

class CustomerInfo(BaseModel):
    name: str
    email: EmailStr
    address: str
    city: Optional[str] = None
    country: Optional[str] = None

class Order(BaseModel):
    """
    Collection: order
    Stores checkout orders
    """
    items: List[OrderItem]
    customer: CustomerInfo
    total: float = Field(..., ge=0)
    notes: Optional[str] = None
