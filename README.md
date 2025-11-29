# LLM Quiz Solver (FastAPI + Playwright)

A fully automated quiz executor built for the **IIT Madras TDS – LLM Analysis Project**.  
This system accepts quiz tasks through a POST API, extracts questions from JavaScript-rendered HTML pages using a headless browser, processes multi-step tasks, and submits correct answers back to the evaluation server automatically.

---

## 🚀 Features

### 🔍 Intelligent Scraping
- Renders dynamic & JavaScript-based pages using **Playwright**  
- Extracts:
  - relative & absolute URLs  
  - quiz instructions  
  - hidden `<pre>` blocks  
  - submit endpoints  
  - task metadata  

### ⚙ Automated Multi-Step Solving
- Follows the server's workflow:
  1. Receive incoming quiz URL  
  2. Scrape question content  
  3. Solve the required data task  
  4. POST answer to the provided submit endpoint  
  5. Continue through chained quiz URLs  
  6. Stop automatically when no new URL is provided  

### 🧠 Modular Architecture
- `scraper.py` → Page scraping & submit URL detection  
- `solver.py` → Multi-step answer execution  
- `utils.py` → Helper functions for answer extraction  
- `main.py` → FastAPI server  

### 🖥 Windows-Compatible Execution
Playwright is executed using **sync mode inside a ThreadPoolExecutor**, making the system fully compatible with Windows machines for local debugging.

### 🧪 Local Testing Support
Includes a `test_api.py` to validate your endpoint with the demo quiz server.

---

## 📡 API Usage

### POST `/quiz`

**Request JSON:**
```json
{
  "email": "your_email",
  "secret": "your_secret_key",
  "url": "first_quiz_url"
}

Response JSON:

{
  "success": true,
  "answer": "<final answer submitted>"
}

📁 Project Structure
.
├── app/
│   ├── main.py
│   ├── solver.py
│   ├── scraper.py
│   ├── utils.py
│   ├── config.py
│   └── __init__.py
├── tests/
│   ├── test_api.py
│   └── test_flow.py
├── README.md
├── requirements.txt
├── deployment_instructions.md
├── LICENSE
└── .gitignore

🔐 Environment Variables

Create a .env file:

SECRET_KEY=your_secret_here
OPENAI_API_KEY=your_openai_key_here
AIPIPE_KEY=your_aipipe_token_if_needed


These values must not be committed to GitHub.

🧪 Local Testing

Start the server:

uvicorn app.main:app --reload


Run test script:

python test_api.py

📄 License

This project is released under the MIT License, as required for submission.

👤 Author

Developed for the IIT Madras BSc Degree Program – LLM Analysis Project.


---

# 📄 **deployment_instructions.md (FINAL VERSION — COPY THIS)**

```markdown
# Deployment Instructions (Render)

This guide explains how to deploy the **LLM Quiz Solver (FastAPI + Playwright)** to Render, as required for the IITM TDS LLM Analysis project.

---

## 1. Create a New Web Service

Visit:  
https://dashboard.render.com/

Click **New → Web Service**  
Select **your GitHub repository** containing this project.

---

## 2. Configure Service

### ✔ Runtime


Python 3.x


### ✔ Build Command


pip install -r requirements.txt && playwright install chromium


### ✔ Start Command


uvicorn app.main:app --host 0.0.0.0 --port 10000


### ✔ Port


10000


Render automatically detects this.

---

## 3. Environment Variables

Go to:

**Render → Service → Environment → Add Environment Variable**

Add:

| Key | Value |
|-----|--------|
| SECRET_KEY | the secret you submitted in the Google Form |
| OPENAI_API_KEY | your OpenAI key (if your quiz tasks need LLM) |
| AIPIPE_KEY | only if you use audio transcription tasks |

---

## 4. Set Instance Type

**Free Tier** is enough.

---

## 5. Deploy

Click **Deploy**.  
Wait until build completes and service turns green.

Your deployed API URL will be like:



https://llm-quiz-solver.onrender.com/quiz


This URL is what you will submit in the Google Form.

---

## 6. Test Your Deployment (Recommended)

Use the demo quiz server to verify the service:



POST <your_render_url>/quiz


Payload:
```json
{
  "email": "your_email",
  "secret": "your_secret",
  "url": "https://tds-llm-analysis.s-anand.net/demo"
}


You should receive:

{"success": true, "answer": "..."}