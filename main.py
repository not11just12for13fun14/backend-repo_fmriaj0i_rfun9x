import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from database import db, create_document, get_documents
from schemas import Product, Order

app = FastAPI(title="Pet Harness Store API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Pet Harness Store Backend Running"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
                response["connection_status"] = "Connected"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

# Public catalog endpoints
@app.get("/api/products", response_model=List[Product])
def list_products(species: Optional[str] = None, size: Optional[str] = None):
    filter_dict = {}
    if species:
        filter_dict["species"] = species
    # Size filter: products whose sizes array contains the requested size
    if size:
        filter_dict["sizes"] = {"$in": [size]}

    docs = get_documents("product", filter_dict)
    # Convert MongoDB docs (with _id) to Product by mapping fields; ignore unknown keys
    products: List[Product] = []
    for d in docs:
        d.pop("_id", None)
        try:
            products.append(Product(**d))
        except Exception:
            # Skip documents that don't validate
            continue
    return products

@app.post("/api/products", status_code=201)
def create_product(product: Product):
    try:
        _id = create_document("product", product)
        return {"id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Orders
@app.post("/api/orders", status_code=201)
def create_order(order: Order):
    try:
        _id = create_document("order", order)
        return {"id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
