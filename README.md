# TrueLineQA 📄

> Upload a PDF. Ask questions. Get instant AI-powered answers.

TrueLineQA is a Streamlit web app that lets you chat with your PDF documents. Powered by **Groq's LLaMA 3.1** model, it reads your document and answers questions based strictly on its content — no hallucinations, no guessing.

---

## What It Does

- Upload any PDF and start a conversation with it
- Ask questions in plain English and get precise answers
- Secure user accounts with encrypted passwords
- All your chats are saved — pick up where you left off
- Manage and delete past chats from the sidebar
- Runs fully containerized with Docker — one command setup

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| AI Model | Groq API — LLaMA 3.1 8B Instant |
| Database | MongoDB |
| PDF Parsing | pdfplumber |
| Authentication | bcrypt |
| Containerization | Docker + Docker Compose |

---

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your machine
- A free Groq API key → [Get one here](https://console.groq.com/)

---

### 1. Set up your Groq API key
TrueLineQA uses Groq's LLM API to generate answers from uploaded PDFs.

- Create a Groq Account
- Visit:(https://console.groq.com)
- Generate API key:(https://console.groq.com/keys) Click and Create

### 2. Add the Groq API Key
- Open : app.py
- Replace :  "Authorization": "Bearer YOUR_API_KEY"

### 3. Install Docker Desktop
- Windows : https://www.docker.com/products/docker-desktop

### 4. Start Docker Desktop
- After installation:Open Docker Desktop
- Wait until Docker starts successfully,You should see: Docker Engine Running

### 5. Open Terminal
- Navigate to the TrueLineQA project folder.
- Open Command Prompt or PowerShell: cd path\to\AuraDoc

### 6. Build and Run the application
- Run: docker-compose up --build
- This command:

1. Builds the Docker image
2. Installs Python dependencies
3. Starts the TrueLineQA container
4. Starts MongoDB container
5. Connects both containers automatically

### 7. Verify Successful Startup & Open the Application
- You can now view your Streamlit app in your browser : Local URL: http://localhost:8501
- Open your browser and visit: http://localhost:8501

---

## Security

- Passwords are hashed using **bcrypt** before storage — never stored in plain text

---

Built by Atharv Wagh.
