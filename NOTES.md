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

## 6. Deployment

### Backend — Render (recommended)

1. Push your repo to GitHub
2. Go to https://render.com → **New → Web Service**
3. Connect your repo and set:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Python 3
4. Add environment variables in the Render dashboard (same keys as `backend/.env`):
   ```
   MONGODB_URI=...
   SECRET_KEY=...
   GROQ_API_KEY=...
   JWT_ALGORITHM=HS256
   JWT_EXPIRE_DAYS=7
   ```
5. The `backend/Procfile` is already configured for this setup

> **Note**: The `model/` and `backend/chroma_db/` directories must be committed to the repo — Render needs them at runtime.

---

### Frontend — Vercel (recommended)

1. Go to https://vercel.com → **New Project** → import your repo
2. Set:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
3. Add environment variable:
   ```
   VITE_API_URL=https://your-render-backend-url.onrender.com
   ```
4. Deploy — Vercel auto-deploys on every push to `main`

---

### Alternative: Heroku (backend)

The `Procfile` at `backend/Procfile` is already set up for Heroku:

```bash
heroku create your-app-name
heroku config:set MONGODB_URI=... SECRET_KEY=... GROQ_API_KEY=...
git subtree push --prefix backend heroku main
```

---

### Alternative: Railway

1. New project → Deploy from GitHub repo
2. Set root to `backend`, add the same env vars as above
3. Railway auto-detects the `Procfile`

---

## External Accounts Needed

| Service | Purpose | Free Tier |
|---|---|---|
| MongoDB Atlas | Database | Yes |
| Groq | LLM for study coach | Yes |
