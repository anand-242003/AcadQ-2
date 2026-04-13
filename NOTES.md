# Setup Notes for New Contributors

## Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- pip

---

## 1. Clone the Repo

```bash
git clone https://github.com/<your-org>/acadiq.git
cd acadiq
```

---

## 2. Backend Setup

Install Python dependencies:

```bash
cd backend
pip install -r requirements.txt
```

Copy the env file and fill in the values:

```bash
cp .env.example .env
```

Open `backend/.env` and set the following:

```
MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
SECRET_KEY=any-random-string-at-least-32-characters
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
JWT_ALGORITHM=HS256
JWT_EXPIRE_DAYS=7
```

- **MONGODB_URI** — create a free cluster at https://www.mongodb.com/atlas and grab the connection string
- **GROQ_API_KEY** — get a free key at https://console.groq.com
- **SECRET_KEY** — just make up any long random string

---

## 3. Frontend Setup

Install Node dependencies:

```bash
cd frontend
npm install
```

Copy the env file:

```bash
cp .env.example .env
```

The default value is fine for local development:

```
VITE_API_URL=http://localhost:8000
```

---

## 4. Model Files

The `model/` directory already has all `.pkl` files committed — no retraining needed.

The ChromaDB vector store in `backend/chroma_db/` is also committed, so RAG works out of the box.

---

## 5. Running the App

Start the backend:

```bash
cd backend
uvicorn main:app --reload
```

Start the frontend (in a separate terminal):

```bash
cd frontend
npm run dev
```

Frontend runs at http://localhost:5173, backend at http://localhost:8000.

---

## External Accounts Needed

| Service | Purpose | Free Tier |
|---|---|---|
| MongoDB Atlas | Database | Yes |
| Groq | LLM for study coach | Yes |
