from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from app.models.schemas import UserPreferences, MatchResponse
from app.services.matcher_service import match_pet

app = FastAPI(
    title="Pet Adoption Matcher API",
    description="Find your ideal cat or dog based on personality matching",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files and templates for UI
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/images", StaticFiles(directory="data/images"), name="images")  # Your buddy's image mounting
templates = Jinja2Templates(directory="app/templates")

# ===== IMAGE SERVING (Your buddy's code) =====

@app.get("/image/{pet_type}/{filename}")
def get_pet_image(pet_type: str, filename: str):
    """
    Serve pet images from the local data/images directory.
    """
    # Validate pet type
    if pet_type not in ["dog", "cat"]:
        raise HTTPException(status_code=400, detail="pet_type must be 'dog' or 'cat'")
    
    # Construct file path - updated to match your buddy's structure
    image_path = Path(f"data/images/{pet_type}s/{filename}")
    
    # Check if file exists
    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    
    # Return the image file
    return FileResponse(image_path)

# ===== API ENDPOINTS =====

@app.post("/match_pet", response_model=MatchResponse)
def match_pet_endpoint(user_input: UserPreferences):
    """
    Takes user questionnaire data and returns the best pet matches.
    
    The user input should include:
    - pet_type: "dog" or "cat"
    - dogs, cats, kids: comfort levels (1-5)
    - energy, affection, training: preference levels (1-5)
    """
    try:
        result = match_pet(user_input.dict())
        return MatchResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# ===== UI ROUTES =====

@app.get("/")
def root():
    """Redirect to the UI landing page"""
    return RedirectResponse(url="/friendr")

@app.get("/friendr", response_class=HTMLResponse)
async def landing_page(request: Request):
    """Main landing page with dog/cat selection"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/friendr/quiz", response_class=HTMLResponse)
async def quiz_page(request: Request, type: str = "dog"):
    """Quiz page for dogs or cats"""
    if type not in ["dog", "cat"]:
        raise HTTPException(status_code=400, detail="Invalid pet type")
    return templates.TemplateResponse("quiz.html", {
        "request": request, 
        "pet_type": type
    })

@app.get("/friendr/results", response_class=HTMLResponse)
async def results_page(request: Request, type: str = "dog"):
    """Results page showing pet matches"""
    if type not in ["dog", "cat"]:
        raise HTTPException(status_code=400, detail="Invalid pet type")
    return templates.TemplateResponse("results.html", {
        "request": request, 
        "pet_type": type
    })

# ===== API ENDPOINTS FOR UI =====

@app.post("/friendr/api/match", response_model=MatchResponse)
def ui_match_endpoint(user_input: UserPreferences):
    """API endpoint specifically for the UI to call"""
    try:
        result = match_pet(user_input.dict())
        return MatchResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/friendr/quiz/submit")
async def submit_quiz_ui(request: Request):
    """Handle quiz submission from UI"""
    try:
        # Get form data
        form_data = await request.json()
        
        # Convert to UserPreferences format
        user_prefs = UserPreferences(
            pet_type=form_data.get("pet_type", "dog"),
            dogs=form_data.get("dogs", 3),
            cats=form_data.get("cats", 3),
            kids=form_data.get("kids", 3),
            energy=form_data.get("energy", 3),
            affection=form_data.get("affection", 3),
            training=form_data.get("training", 3)
        )
        
        # Get matches
        result = match_pet(user_prefs.dict())
        return MatchResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing quiz: {str(e)}")

# ===== TEST ROUTES =====

@app.get("/test", response_class=HTMLResponse)
async def test_page():
    """Simple test page to verify HTML serving works"""
    return """
    <html>
        <head>
            <title>Friendr Test Page</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    text-align: center;
                    padding: 50px;
                }
                .button {
                    background: white;
                    color: #667eea;
                    padding: 15px 30px;
                    border: none;
                    border-radius: 25px;
                    font-size: 18px;
                    margin: 10px;
                    cursor: pointer;
                    text-decoration: none;
                    display: inline-block;
                }
                .button:hover { background: #f0f0f0; }
            </style>
        </head>
        <body>
            <h1>🐾 Friendr Test Page</h1>
            <p>If you see this, HTML serving is working!</p>
            
            <div style="margin-top: 30px;">
                <a href="/friendr" class="button">🏠 Go to Landing Page</a>
                <a href="/docs" class="button">📚 API Docs</a>
                <a href="/health" class="button">💚 Health Check</a>
            </div>
            
            <div style="margin-top: 30px; font-size: 14px;">
                <p><strong>Available URLs:</strong></p>
                <p>🏠 Landing: <code>/friendr</code></p>
                <p>🐕 Dog Quiz: <code>/friendr/quiz?type=dog</code></p>
                <p>🐱 Cat Quiz: <code>/friendr/quiz?type=cat</code></p>
                <p>🔧 API: <code>/match_pet</code></p>
                <p>🖼️ Test Image: <code>/image/cat/cat_332.jpg</code></p>
            </div>
        </body>
    </html>
    """

@app.get("/api-info")
def api_info():
    """API information endpoint"""
    return {
        "message": "Pet Adoption Matcher API",
        "version": "1.0.0",
        "endpoints": {
            "ui": {
                "landing": "/friendr",
                "dog_quiz": "/friendr/quiz?type=dog",
                "cat_quiz": "/friendr/quiz?type=cat",
                "results": "/friendr/results?type=dog"
            },
            "api": {
                "match_pet": "/match_pet",
                "health": "/health",
                "docs": "/docs"
            },
            "images": {
                "example": "/image/cat/cat_332.jpg",
                "pattern": "/image/{pet_type}/{filename}"
            }
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)