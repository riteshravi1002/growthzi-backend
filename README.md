# 💼 Growthzi Backend Developer Assignment

A professional and secure Flask-based backend system built for Growthzi. This project enables authenticated users to generate AI-powered website content, preview it in a responsive interface, and manage/export their data seamlessly.

---

## 🌐 Live Deployment

🚀 **[Live API on Render](https://growthzi-backend.onrender.com)**

> Access is via secure API endpoints. See below for usage with Postman.

---

## ✅ Key Features

- 🔐 **JWT-Based User Authentication**
- 🧠 **AI-Powered Content Generation via OpenRouter (OpenAI-Compatible)**
- 📂 **MongoDB Integration for Persistent Storage**
- 🖼️ **Dynamic HTML Previews with Tailwind CSS**
- 📄 **Export Generated Content to Downloadable HTML**
- 🧹 **Admin Cleanup & Data Management Endpoints**

---

## ⚙️ Technology Stack

- **Backend:** Python, Flask
- **Database:** MongoDB (via Flask-PyMongo)
- **Authentication:** JWT (Flask-JWT-Extended)
- **AI Integration:** OpenRouter API (compatible with OpenAI SDK)
- **Frontend Previews:** Tailwind CSS
- **Deployment:** Render (Production-grade WSGI with Gunicorn)

---

## 🚀 Quick Start (Local Setup)

```bash
# 1. Clone the repository
https://github.com/riteshravi1002/growthzi-backend.git
cd growthzi-backend

# 2. Create a virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create and configure environment variables
cp .env.example .env
```

### ✨ Example `.env` Configuration
```ini
MONGO_URI=mongodb://localhost:27017/growthzi
JWT_SECRET_KEY=your_jwt_secret_key
OPENAI_API_KEY=your_openrouter_api_key
```

---

## 📬 API Endpoints

### 🔐 Authentication
| Method | Endpoint     | Description              |
|--------|--------------|--------------------------|
| POST   | `/auth/signup` | Register new users       |
| POST   | `/auth/login`  | Log in & receive JWT     |

### ✨ Generate & Manage Content
| Method | Endpoint                          | Description                          |
|--------|-----------------------------------|--------------------------------------|
| POST   | `/generate/`                      | Generate website content (JWT)       |
| GET    | `/generate/list`                  | List user-generated sites (JWT)      |
| GET    | `/generate/preview/<id>`          | View live HTML preview               |
| GET    | `/generate/export/<id>.html`      | Download exported HTML file (JWT)   |
| DELETE | `/generate/delete/<id>`           | Remove generated content (JWT)       |

---

## 🔐 Using with Postman

1. **Signup/Login** to receive a JWT token.
2. Add this header to every `/generate/*` request:
   ```http
   Authorization: Bearer <your_token>
   ```
3. Test POST requests like:
   ```json
   POST /generate/
   {
     "business_type": "Bakery",
     "industry": "Food"
   }
   ```

✅ Token required for protected endpoints.

---

## 📸 Screenshots (UI & Preview)

<p align="center">
  <img src="screenshots/signup.png" width="420">
  <img src="screenshots/postman-generate.png" width="420">
  <br>
  <img src="screenshots/preview-page.png" width="600">
  <br>
  <img src="screenshots/custom-preview-upload.png" width="600">
</p>

---

## 📝 Project Structure

```
growthzi-backend/
├── app/
│   ├── __init__.py         # App factory & blueprint registration
│   ├── auth.py             # Signup/Login logic
│   ├── generate.py         # Content generation, preview, export
│   ├── config.py           # Env configuration
│   └── templates/          # HTML templates (Jinja2 + Tailwind)
│       ├── index.html
│       ├── preview.html
│       └── list.html
├── run.py                  # App entry point
├── .env.example            # Environment setup guide
├── requirements.txt        # Dependencies
└── README.md               # You're here 😁
```

---

## 📦 Production-Ready Highlights

- 🌐 Deployed on [Render](https://render.com/)
- 📁 Modular project structure (blueprints)
- 🔒 JWT-secured routes
- 🧠 AI content via OpenRouter
- 💃 MongoDB persistence with timestamps & user binding
- 📄 Export functionality with clean HTML templates

---

## ⚖️ GitHub Repository

> 📍 [github.com/riteshravi1002/growthzi-backend](https://github.com/riteshravi1002/growthzi-backend)

---

## ✅ Final Submission Notes

- [x] Backend API with secure auth
- [x] Smart AI content generation
- [x] HTML preview page
- [x] Export & delete functionality
- [x] Render live deployment
- [x] Clean documentation & .env.example

🌟 This project fulfills all technical and functional requirements of the **Growthzi Backend Developer Assignment**.

---

> Crafted with dedication by [@riteshravi1002](https://github.com/riteshravi1002) — Let’s build something impactful!

