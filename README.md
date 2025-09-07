# 🐾 Friendr - Pet Adoption Matcher

A full-stack FastAPI application with a beautiful web interface that uses machine learning to match users with their ideal pets based on personality compatibility. Built with K-means clustering, featuring both REST API and interactive web UI.

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Web Interface](#web-interface)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Development](#development)
- [Contributing](#contributing)

## ✨ Features

- **Smart Pet Matching**: Uses K-means clustering to find compatible pets based on user preferences
- **Dual Pet Support**: Separate models for dogs and cats
- **Beautiful Web Interface**: Interactive quiz with responsive design
- **RESTful API**: Clean FastAPI endpoints with automatic documentation
- **Data Validation**: Pydantic models ensure data integrity
- **Image Serving**: Local image hosting through FastAPI endpoints
- **CORS Support**: Cross-origin requests enabled for frontend integration
- **Scalable Architecture**: Modular design following SOLID principles

## 🏗️ Architecture

```
friendr/
├── app/                    # FastAPI application
│   ├── main.py            # Application entry point with UI routes
│   ├── models/            # Pydantic data models
│   ├── services/          # Business logic layer
│   ├── utils/             # Utility functions
│   ├── static/            # Frontend assets
│   │   ├── css/           # Stylesheets
│   │   └── js/            # JavaScript files
│   └── templates/         # HTML templates
│       ├── base.html      # Base template
│       ├── index.html     # Landing page
│       ├── quiz.html      # Pet quiz page
│       └── results.html   # Results page
├── ml_model/              # Machine learning components
│   ├── trainer.py         # Model training
│   └── predictor.py       # Model inference
├── data/                  # Data storage
│   ├── pet_data.csv       # Pet characteristics
│   ├── user_data.csv      # User preferences
│   └── images/            # Pet images (dogs/ & cats/)
└── saved_models/          # Trained ML models
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone the Repository

```bash
git clone https://github.com/michaelige1/friendr.git
cd friendr
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Train the Models

```bash
python -m ml_model.trainer
```

This will create the necessary K-means models in the `saved_models/` directory.

## 🎯 Usage

### Starting the Server

```bash
# Make sure your virtual environment is activated
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Start the FastAPI server
python -m uvicorn app.main:app --reload
```

The server will start at `http://localhost:8000`

### Web Interface

Once the server is running, you can access:

- **🏠 Landing Page**: `http://localhost:8000/friendr`
- **🐕 Dog Quiz**: `http://localhost:8000/friendr/quiz?type=dog`
- **🐱 Cat Quiz**: `http://localhost:8000/friendr/quiz?type=cat`
- **📊 Results**: `http://localhost:8000/friendr/results`
- **🧪 Test Page**: `http://localhost:8000/test`

### Interactive API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **API Info**: `http://localhost:8000/api-info`

## 🌐 Web Interface

### Landing Page (`/friendr`)
- Beautiful gradient background with pet selection
- Choose between finding a dog or cat
- Responsive design with hover effects
- Direct links to quiz pages

### Quiz Pages (`/friendr/quiz`)
- Interactive personality assessment
- 6-question compatibility quiz
- Real-time form validation
- Dynamic pet type selection (dog/cat)

### Results Page (`/friendr/results`)
- Displays top 6 pet matches
- Shows pet images, names, ages, and compatibility percentages
- Responsive card layout
- Direct links to restart quiz

### Features
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern UI**: Built with Tailwind CSS
- **Interactive Elements**: Alpine.js for dynamic behavior
- **Smooth Animations**: CSS transitions and hover effects
- **Image Integration**: Local pet images served via FastAPI

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Web Interface Endpoints

#### 1. Landing Page
```http
GET /friendr
```
Returns the main landing page with pet selection.

#### 2. Quiz Pages
```http
GET /friendr/quiz?type=dog
GET /friendr/quiz?type=cat
```
Returns interactive quiz pages for dogs or cats.

#### 3. Results Page
```http
GET /friendr/results?type=dog
```
Returns results page showing pet matches.

### API Endpoints

#### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy"
}
```

#### 2. Pet Matching (API)
```http
POST /match_pet
```

**Request Body:**
```json
{
  "pet_type": "dog",
  "dogs": 4,
  "cats": 2,
  "kids": 5,
  "energy": 3,
  "affection": 4,
  "training": 3
}
```

**Field Descriptions:**
- `pet_type`: Type of pet ("dog" or "cat")
- `dogs`: Comfort level with dogs (1-5 scale)
- `cats`: Comfort level with cats (1-5 scale)
- `kids`: Comfort level with kids (1-5 scale)
- `energy`: Energy level preference (1-5 scale)
- `affection`: Affection level preference (1-5 scale)
- `training`: Training commitment level (1-5 scale)

**Response:**
```json
{
  "matches": [
    {
      "name": "Daisy",
      "type": "dog",
      "age": 10,
      "match_percentage": 97.88,
      "image_url": "http://localhost:8000/image/dog/dog_462.jpg"
    },
    {
      "name": "Charlie",
      "type": "dog", 
      "age": 13,
      "match_percentage": 97.88,
      "image_url": "http://localhost:8000/image/dog/dog_258.jpg"
    },
    {
      "name": "Ace",
      "type": "dog",
      "age": 13,
      "match_percentage": 92.21,
      "image_url": "http://localhost:8000/image/dog/dog_464.jpg"
    }
  ]
}
```

**Response Field Descriptions:**
- `name`: Pet's name
- `type`: Pet type ("dog" or "cat")
- `age`: Pet's age in years (converted from months)
- `match_percentage`: Compatibility percentage (boosted for demo purposes)
- `image_url`: Direct URL to pet's image

#### 3. UI-Specific API Endpoint
```http
POST /friendr/api/match
```
Same as `/match_pet` but specifically designed for UI integration.

#### 4. Quiz Submission (UI)
```http
POST /friendr/quiz/submit
```
Handles quiz form submissions from the web interface.

#### 5. Image Serving
```http
GET /image/{pet_type}/{filename}
```

**Parameters:**
- `pet_type`: "dog" or "cat"
- `filename`: Image filename (e.g., "dog_462.jpg")

**Response:** Returns the image file directly

**Example:**
```http
GET /image/dog/dog_462.jpg
```

#### 6. API Information
```http
GET /api-info
```
Returns comprehensive API documentation and available endpoints.

## 🧪 Testing

### Web Interface Testing

1. **Start the server:**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

2. **Open your browser and visit:**
   - `http://localhost:8000/friendr` - Landing page
   - `http://localhost:8000/friendr/quiz?type=dog` - Dog quiz
   - `http://localhost:8000/friendr/quiz?type=cat` - Cat quiz

3. **Complete the quiz and view results**

### Manual API Testing with cURL

```bash
# Health check
curl http://localhost:8000/health

# Pet matching example
curl -X POST "http://localhost:8000/match_pet" \
     -H "Content-Type: application/json" \
     -d '{
       "pet_type": "cat",
       "dogs": 3,
       "cats": 5,
       "kids": 4,
       "energy": 2,
       "affection": 5,
       "training": 2
     }'

# Test image serving
curl http://localhost:8000/image/dog/dog_462.jpg

# API information
curl http://localhost:8000/api-info
```

### Testing with Python requests

```python
import requests

# Test pet matching
response = requests.post(
    "http://localhost:8000/match_pet",
    json={
        "pet_type": "dog",
        "dogs": 4,
        "cats": 2,
        "kids": 5,
        "energy": 3,
        "affection": 4,
        "training": 3
    }
)

print(response.json())

# Test image serving
image_response = requests.get("http://localhost:8000/image/dog/dog_462.jpg")
print(f"Image size: {len(image_response.content)} bytes")
```

## 🔧 Development

### Project Structure Benefits

- **Full-Stack Integration**: Seamless API and web interface
- **Modular Design**: Easy to add new features or modify existing ones
- **Separation of Concerns**: Clear boundaries between data, business logic, API, and UI layers
- **Testability**: Each component can be tested independently
- **Maintainability**: Changes in one area don't affect others

### Frontend Technologies

- **Tailwind CSS**: Utility-first CSS framework for responsive design
- **Alpine.js**: Lightweight JavaScript framework for interactivity
- **HTMX**: Modern HTML over the wire for dynamic content
- **Jinja2**: Template engine for server-side rendering

### Adding New Features

1. **New Pet Types**: Add to the `pet_type` literal in schemas
2. **New Matching Criteria**: Extend the feature columns in trainer and predictor
3. **New API Endpoints**: Add to `app/main.py` following existing patterns
4. **New UI Pages**: Create templates in `app/templates/` and add routes
5. **New Services**: Create in `app/services/` with proper abstractions

### Data Processing Notes

- **Age Conversion**: Pet ages are stored in months but returned in years (rounded)
- **Match Percentage Boosting**: Demo version adds 40% to match percentages for better presentation
- **Duplicate Handling**: Pets with identical personality profiles are deduplicated
- **Image Assignment**: Each pet gets one unique image from the local image collection

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Common Issues

1. **Model not found error**: Run `python -m ml_model.trainer` to generate models
2. **Import errors**: Ensure virtual environment is activated
3. **Port already in use**: Change port with `uvicorn app.main:app --port 8001`
4. **Image not found**: Ensure images are in `data/images/dogs/` and `data/images/cats/`
5. **uvicorn command not found**: Use `python -m uvicorn` instead of just `uvicorn`
6. **Template not found**: Ensure `app/templates/` directory exists with HTML files
7. **Static files not loading**: Check that `app/static/` directory exists with CSS/JS files

### Server Startup Issues

If you encounter issues starting the server:

```bash
# Check if port is in use
lsof -i :8000

# Kill existing processes
pkill -f uvicorn

# Start with verbose output
python -m uvicorn app.main:app --reload --log-level debug
```

### Support

For support, please open an issue on [GitHub](https://github.com/michaelige1/friendr/issues).

---

**Made with ❤️ for pet lovers everywhere**
