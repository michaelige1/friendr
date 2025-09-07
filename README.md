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
      "size": "Medium",
      "weight": 32.7,
      "energy": 3,
      "affection": 4,
      "training": 4,
      "type": "dog",
      "age": 10,
      "match_percentage": 97.88,
      "image_url": "http://localhost:8000/image/dog/dog_462.jpg"
    },
    {
      "name": "Charlie",
      "size": "Medium",
      "weight": 31.2,
      "energy": 3,
      "affection": 4,
      "training": 4,
      "type": "dog", 
      "age": 13,
      "match_percentage": 97.88,
      "image_url": "http://localhost:8000/image/dog/dog_258.jpg"
    },
    {
      "name": "Ace",
      "size": "Large",
      "weight": 71.8,
      "energy": 4,
      "affection": 4,
      "training": 4,
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
- `size`: Pet's size (Small, Medium, Large)
- `weight`: Pet's weight in pounds
- `energy`: Pet's energy level (1-5 scale)
- `affection`: Pet's affection level (1-5 scale)
- `training`: Pet's training level (1-5 scale)
- `match_percentage`: Compatibility percentage (boosted for demo purposes)
- `image_url`: Direct URL to pet's image