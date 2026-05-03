import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import List

app = FastAPI(title="AURELIA API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Pydantic Models
class CartItem(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
    image_url: str

class PaymentRequest(BaseModel):
    items: List[CartItem]
    total: float

class ChatRequest(BaseModel):
    message: str

class ContactRequest(BaseModel):
    name: str
    email: str
    inquiry: str

# Endpoints

@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")

@app.get("/products")
async def get_products():
    return [
        {
            "id": 1,
            "name": "The Obsidian Trench",
            "price": 1250.00,
            "image_url": "/static/images/trench.png"
        },
        {
            "id": 2,
            "name": "Champagne Silk Blouse",
            "price": 890.00,
            "image_url": "/static/images/blouse.png"
        },
        {
            "id": 3,
            "name": "Cashmere Turtleneck",
            "price": 1050.00,
            "image_url": "/static/images/turtleneck.png"
        },
        {
            "id": 4,
            "name": "Leather Handbag",
            "price": 2400.00,
            "image_url": "/static/images/handbag.jpg"
        },
        {
            "id": 5,
            "name": "Midnight Blue Evening Gown",
            "price": 1850.00,
            "image_url": "/static/images/gown.jpg"
        },
        {
            "id": 6,
            "name": "Classic Aviator Sunglasses",
            "price": 420.00,
            "image_url": "/static/images/sunglasses.png"
        },
        {
            "id": 7,
            "name": "Chronograph Automatic Watch",
            "price": 3500.00,
            "image_url": "/static/images/watch.png"
        },
        {
            "id": 8,
            "name": "Aurelia Signature Parfum",
            "price": 280.00,
            "image_url": "/static/images/parfum.png"
        },
        {
            "id": 9,
            "name": "Velvet Loafers",
            "price": 790.00,
            "image_url": "/static/images/loafers.png"
        },
        {
            "id": 10,
            "name": "Gold Vermeil Hoop Earrings",
            "price": 540.00,
            "image_url": "/static/images/hoops.png"
        }
    ]

@app.post("/process-payment")
async def process_payment(request: PaymentRequest):
    # Simulate payment processing delay
    await asyncio.sleep(2)
    return {"status": "success", "message": "Payment Successful. Thank you for shopping with AURELIA."}

@app.post("/chat")
async def chat(request: ChatRequest):
    msg = request.message.lower()
    
    # Keyword matching for the AI Concierge
    if "material" in msg or "fabric" in msg:
        response = "Our garments are crafted from the finest materials, including Italian silk and hand-sourced cashmere, designed for unparalleled elegance."
    elif "shipping" in msg or "delivery" in msg:
        response = "We offer complimentary worldwide shipping on all AURELIA orders via secure courier."
    elif "price" in msg or "cost" in msg:
        response = "Our pieces reflect true craftsmanship and exclusivity. You can view individual pricing in our collection."
    elif "hello" in msg or "hi" in msg:
        response = "Welcome to AURELIA. I am your personal concierge. How may I assist you with your wardrobe today?"
    else:
        response = "I am here to assist you with any inquiries regarding our collections, materials, or your personal styling needs."
        
    return {"response": response}

@app.post("/contact-submit")
async def contact_submit(request: ContactRequest):
    # In a real scenario, this would send an email or save to a DB
    return {"status": "success", "message": f"Thank you, {request.name}. Your inquiry has been received by our client services team."}

# Mount static files last so API routes take precedence
app.mount("/static", StaticFiles(directory="static"), name="static")
