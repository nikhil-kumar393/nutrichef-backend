# 🚀 NutriChef.ai Backend API

A production-ready backend API for **NutriChef.ai**, built with **FastAPI**, **Python**, and **Machine Learning**. The backend processes user ingredients, predicts recipe categories using a custom Scikit-Learn model, and leverages **Google Gemini AI** to generate personalized recipes and nutrition insights.

🌐 **Live API:** https://nutrichef-ai.onrender.com

📖 **API Documentation (Swagger UI):**
https://nutrichef-ai.onrender.com/docs

---

## ✨ Features

* ⚡ High-performance REST API built with FastAPI
* 🤖 Hybrid AI engine using Scikit-Learn + Google Gemini AI
* 🧠 Custom-trained Machine Learning model
* 📊 Nutrition-aware recipe generation
* 🔒 CORS configured for secure frontend communication
* 📄 Automatic OpenAPI & Swagger documentation
* ☁️ Production deployment on Render

---

## 🛠 Tech Stack

### Backend

* FastAPI
* Python
* Uvicorn

### AI & Machine Learning

* Scikit-Learn
* Joblib
* Google Gemini API

### Deployment

* Render

---

## 📡 API Endpoints

### 🔹 Generate Recipe

**POST** `/get_recipe`

#### Request

```json
{
  "ingredients": [
    "eggs",
    "tomato",
    "onion"
  ]
}
```

#### Response

```json
{
  "recipe": "...",
  "nutrition": "...",
  "estimated_time": "20 mins"
}
```

---

### 🔹 API Documentation

**GET** `/docs`

Interactive Swagger UI for testing API endpoints directly from the browser.

---

## 🚀 Getting Started

### 📋 Prerequisites

Before running the backend locally, make sure you have:

* Python 3.10 or later
* pip
* Google Gemini API Key

---

### ⚙️ Installation

#### 1️⃣ Clone the repository

```bash
git clone https://github.com/nikhil-kumar393/nutrichef-backend.git
```

#### 2️⃣ Navigate to the project folder

```bash
cd nutrichef-backend
```

#### 3️⃣ Create a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 4️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

#### 5️⃣ Create a `.env` file

```env
GEMINI_API_KEY=your_google_gemini_api_key
```

#### 6️⃣ Run the development server

```bash
uvicorn main:app --reload
```

Open your browser and visit:

```text
http://127.0.0.1:8000/docs
```

---

## 📂 Project Structure

```text
nutrichef-backend/
│
├── models/
├── routes/
├── utils/
├── main.py
├── requirements.txt
├── .env
└── README.md
```

---

## 🌐 Deployment

| Service           | Platform   |
| ----------------- | ---------- |
| Backend API       | Render     |
| API Documentation | Swagger UI |

---

## 🔗 Related Repository

**Frontend (React + Vite)**

https://github.com/nikhil-kumar393/nutrichef-frontend

---

## 🔮 Future Improvements

* JWT Authentication
* User Accounts
* Recipe History
* Save Favorite Recipes
* Meal Planning API
* Grocery List API
* Image-based Ingredient Recognition
* Docker Support

---

## 👨‍💻 Author

**Nikhil Kumar**

* GitHub: https://github.com/nikhil-kumar393
* LinkedIn: https://www.linkedin.com/in/nikhil3945

---

## ⭐ If you found this project helpful, consider giving it a Star!
