# 🐾 Friendr - Pet Adoption Matcher

A FastAPI-based application that uses machine learning to match users with their ideal pets based on personality compatibility. Built with K-means clustering and designed following SOLID principles.

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Contributing](#contributing)

## ✨ Features

- **Smart Pet Matching**: Uses K-means clustering to find compatible pets based on user preferences
- **Dual Pet Support**: Separate models for dogs and cats
- **RESTful API**: Clean FastAPI endpoints with automatic documentation
- **Data Validation**: Pydantic models ensure data integrity
- **Image Serving**: Local image hosting through FastAPI endpoints
- **Scalable Architecture**: Modular design following SOLID principles

## 🏗️ Architecture

```
friendr/
├── app/                    # FastAPI application
│   ├── main.py            # Application entry point
│   ├── models/            # Pydantic data models
│   ├── services/          # Business logic layer
│   └── utils/             # Utility functions
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
uvicorn app.main:app --reload
```

The server will start at `http://localhost:8000`

### Interactive API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

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

#### 2. Root Endpoint
```http
GET /
```

**Response:**
```json
{
  "message": "Pet Adoption Matcher API",
  "version": "1.0.0"
}
```

#### 3. Pet Matching
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

#### 4. Image Serving
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

## 🧪 Testing

### Manual Testing with cURL

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

- **Modular Design**: Easy to add new features or modify existing ones
- **Separation of Concerns**: Clear boundaries between data, business logic, and API layers
- **Testability**: Each component can be tested independently
- **Maintainability**: Changes in one area don't affect others

### Adding New Features

1. **New Pet Types**: Add to the `pet_type` literal in schemas
2. **New Matching Criteria**: Extend the feature columns in trainer and predictor
3. **New Endpoints**: Add to `app/main.py` following existing patterns
4. **New Services**: Create in `app/services/` with proper abstractions

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

### Support

For support, please open an issue on [GitHub](https://github.com/michaelige1/friendr/issues).

---

**Made with ❤️ for pet lovers everywhere**
