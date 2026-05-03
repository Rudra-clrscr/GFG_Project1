# AURELIA Luxury Fashion Website

A cohesive, multi-page luxury fashion website featuring a storefront, editorial "About" page, "Contact" page, and a Python-powered AI Concierge. Built with an HTML/CSS/JS frontend and a FastAPI backend.

## Features
- **Minimalist Editorial Design:** Obsidian, Champagne Gold, and Pure White color palette.
- **AI Concierge:** A mock AI chat assistant for personalized luxury shopping.
- **Glassmorphism Header:** Persistent navigation across all pages.
- **Scroll Animations:** Fade-in elements for a dynamic feel.
- **Shopping Cart:** Slide-out drawer with persistent `localStorage` support.
- **FastAPI Backend:** Handles product data, simulated payments, contact submissions, and chat logic.

## Project Structure
- `/static` - Frontend files (HTML, CSS, JS)
- `main.py` - FastAPI backend server
- `render.yaml` - Render deployment configuration
- `requirements.txt` - Python dependencies

## Local Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Server:**
   ```bash
   uvicorn main:app --reload
   ```

3. **View the Website:**
   Open your browser and navigate to `http://localhost:8000/static/index.html`

## Deployment
This project is configured for deployment on Render. Simply connect this repository to Render and use the provided `render.yaml` as the blueprint, or set the start command to `uvicorn main:app --host 0.0.0.0 --port $PORT`.
