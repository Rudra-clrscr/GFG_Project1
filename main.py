import asyncio
import os
from dotenv import load_dotenv
from google import genai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import List

# Load environment variables from .env
load_dotenv()

# Define system prompt for the shopping assistant
system_instruction = """You are an exclusive, high-end luxury fashion shopping assistant for the brand AURELIA. 
Your tone should be sophisticated, elegant, polite, and accommodating. 
You assist clients with styling advice, material details, sizing, and general inquiries about AURELIA products. 
Keep your responses concise, luxurious, and highly personalized."""

# Initialize the Gemini Client
gemini_api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_api_key) if gemini_api_key else None
model_id = "gemini-2.5-flash"

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

def local_concierge_response(message: str) -> str:
    msg = message.lower()

    if "material" in msg or "fabric" in msg:
        return "Our garments are crafted from Italian silk, hand-sourced cashmere, fine wool, and supple leather, selected for a refined hand-feel and lasting elegance."
    if "shipping" in msg or "delivery" in msg:
        return "We offer complimentary worldwide shipping on all AURELIA orders via secure courier, with careful packaging for each piece."
    if "price" in msg or "cost" in msg:
        return "Our pieces reflect meticulous craftsmanship and exclusivity. You can view individual pricing throughout the collection."
    if "size" in msg or "fit" in msg:
        return "AURELIA pieces are tailored with a refined silhouette. For a precise fit, I recommend choosing your usual size for relaxed pieces and sizing up for structured outerwear."
    if "style" in msg or "recommend" in msg or "wear" in msg:
        return "For an elegant wardrobe statement, pair the Obsidian Trench with the Champagne Silk Blouse, then finish with the Leather Handbag for quiet polish."
    if "hello" in msg or "hi" in msg:
        return "Welcome to AURELIA. I am your personal concierge. How may I assist you with your wardrobe today?"

    return "I would be delighted to assist with our collections, materials, sizing, shipping, or personal styling recommendations."

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
    # Default message from local concierge logic
    ai_message = local_concierge_response(request.message)

    if client is None:
        return {"response": ai_message}

    try:
        # TIER 1: Try Gemini 2.5 Flash
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=request.message,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_instruction
            )
        )
        return {"response": response.text or ai_message}
    except Exception as e:
        # Check if the error is due to rate limits or quota (429)
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            print("Gemini 2.5 Flash quota hit, trying TIER 2 (Gemini 2.0 Flash Lite)...")
            try:
                # TIER 2: Fallback to Gemini 2.0 Flash Lite
                response = client.models.generate_content(
                    model="gemini-2.0-flash-lite",
                    contents=request.message,
                    config=genai.types.GenerateContentConfig(
                        system_instruction=system_instruction
                    )
                )
                return {"response": response.text or ai_message}
            except Exception as e2:
                print(f"TIER 2 also failed: {e2}")
        else:
            print(f"Gemini API Error: {e}")
            
    # TIER 3: Local Concierge Fallback
    print("Using TIER 3 (Local Concierge) fallback.")
    return {"response": ai_message}

@app.post("/contact-submit")
async def contact_submit(request: ContactRequest):
    # In a real scenario, this would send an email or save to a DB
    return {"status": "success", "message": f"Thank you, {request.name}. Your inquiry has been received by our client services team."}

# Mount static files last so API routes take precedence
app.mount("/static", StaticFiles(directory="static"), name="static")
