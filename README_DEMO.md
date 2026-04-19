# AcadIQ - Intelligent Learning Analytics & AI Study Coach - Viva Preparation Guide

## Project Overview

AcadIQ is a machine learning and AI-powered platform that predicts student academic performance before exams and provides personalized AI coaching to improve outcomes. The system combines classical ML models for prediction with modern LLM-based conversational AI for coaching.

**Core Problem**: Traditional academic systems provide feedback after exams when intervention is impossible. AcadIQ predicts performance before exams using behavioral data, enabling early intervention.

**Solution**: Multi-model ML pipeline (classification, regression, clustering) + RAG-enhanced AI coach powered by LLM.

---

## Technology Stack

**Backend**: FastAPI (Python 3.9+), MongoDB Atlas, JWT Authentication
**Frontend**: React 18, Vite, TailwindCSS, Recharts
**ML Models**: scikit-learn (Logistic Regression, Linear Regression, K-Means)
**AI/LLM**: LangChain, Groq API (Llama 3.3 70B), ChromaDB
**Deployment**: Render (backend), Vercel (frontend)

---

## Core Features

### 1. ML-Powered Predictions
- Score Prediction (0-100 range)
- Pass/Fail Classification with probability scores
- Learner Profiling (4 behavioral archetypes)
- 97.1% overall accuracy

### 2. AI Study Coach
- Conversational AI powered by Llama 3.3 70B
- RAG-enhanced with 45+ curated study resources
- Personalized 7-day study plans
- Session-based memory

### 3. Rich Analytics
- Radar chart comparing student vs dataset average
- Top 3 weakness identification
- Rule-based personalized recommendations
- Prediction history tracking

### 4. Modern Web Interface
- 5-step wizard for data input
- Real-time validation and feedback
- Responsive design
- Results dashboard with visualizations

---

## Machine Learning Pipeline - Complete Workflow

### Phase 1: Data Collection and Preparation

<details>
<summary><b>Dataset Overview - What, Why, Where</b></summary>

**File Location**: `Data/StudentDataset.csv`

**What**: 5000+ student records with 24 features across 5 categories

**Why**: Behavioral and wellness factors significantly impact academic performance beyond just grades

**Feature Categories**:

1. **Academic Performance (3 features)**
   - quiz_avg: Average quiz scores (0-100)
   - assignment_avg: Average assignment scores (0-100)  
   - midterm_score: Midterm exam score (0-100)
   - **Why**: Direct indicators of current academic standing

2. **Time and Engagement (4 features)**
   - study_hours: Daily study hours
   - self_study_hours: Self-directed study time
   - online_classes_hours: Online class attendance
   - topics_completed: Number of topics covered
   - **Why**: Time investment correlates with learning outcomes

3. **Wellness and Lifestyle (4 features)**
   - sleep_hours: Sleep per night (4-12 hours)
   - mental_health_score: Self-reported mental health (1-10)
   - exercise_minutes: Daily physical activity
   - caffeine_intake_mg: Daily caffeine consumption
   - **Why**: Physical and mental health directly affect cognitive performance

4. **Behavioral Indicators (7 features)**
   - social_media_hours: Daily social media usage
   - gaming_hours: Daily gaming time
   - screen_time_hours: Total screen time
   - focus_index: Concentration ability (0-100)
   - productivity_score: Self-reported productivity (0-100)
   - burnout_level: Stress/burnout indicator (0-100)
   - **Why**: Behavioral patterns reveal study quality and distractions

5. **Contextual Variables (6 features)**
   - age: Student age (16-40)
   - gender: Male/Female/Other
   - academic_level: High School/Undergraduate/Postgraduate
   - part_time_job: Yes/No
   - upcoming_deadline: Yes/No
   - internet_quality: Poor/Average/Good/Excellent
   - **Why**: Context affects available time and resources

**Target Variables**:
- exam_score: Continuous score (0-100) for regression
- pass_fail: Binary label (0=Fail, 1=Pass) for classification

</details>

### Phase 2: Model Training Process

<details>
<summary><b>Step 1: Data Preprocessing - What, Why, How</b></summary>

**File Location**: `Notebook/GENAICAPSTONE.ipynb`

**What**: Transform raw data into ML-ready format

**Why**: ML algorithms require numerical, scaled, and clean data

**How**:

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# Load data
df = pd.read_csv('Data/StudentDataset.csv')

# Handle missing values
df.fillna(df.mean(), inplace=True)
```

**Why mean imputation?**: Preserves data distribution, simple and effective for numerical features

**Categorical Encoding**:
```python
df['gender'] = df['gender'].map({'Male': 1, 'Female': 0, 'Other': 2})
df['academic_level'] = df['academic_level'].map({
    'High School': 0, 
    'Undergraduate': 1, 
    'Postgraduate': 1
})
```

**Why label encoding?**: Converts categorical text to numbers that ML models can process

**Feature Engineering**:
```python
# Create derived features
df['total_active_hours'] = df['study_hours'] + df['self_study_hours'] + df['online_classes_hours']
df['total_distraction_hours'] = df['social_media_hours'] + df['gaming_hours']
df['study_distraction_ratio'] = df['study_hours'] / df['total_distraction_hours'].replace(0, 0.1)
df['healthy_sleep'] = df['sleep_hours'].apply(lambda x: 1 if 7 <= x <= 9 else 0)
df['wellness_score'] = (df['mental_health_score'] * 0.4 + 
                        df['sleep_hours'] * 0.3 + 
                        (df['exercise_minutes'] / 60) * 0.3)
df['stress_index'] = (df['burnout_level'] * 0.5 + 
                      df['screen_time_hours'] * 0.3 + 
                      (10 - df['sleep_hours']) * 0.2)
```

**Why feature engineering?**: 
- Captures complex relationships between features
- study_distraction_ratio measures focus quality
- wellness_score combines multiple health indicators
- Improves model performance by providing meaningful derived metrics

**Train/Test Split**:
```python
from sklearn.model_selection import train_test_split

X = df.drop(['exam_score', 'pass_fail'], axis=1)
y_class = df['pass_fail']
y_reg = df['exam_score']

X_train, X_test, y_train, y_test = train_test_split(
    X, y_class, test_size=0.2, random_state=42, stratify=y_class
)
```

**Why stratified split?**: Dataset has 26:1 Fail-to-Pass ratio. Stratification ensures both train and test sets maintain same class distribution.

**Feature Scaling**:
```python
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

**Why StandardScaler?**:
- Features have different scales (age: 16-40, burnout: 0-100)
- Standardization: (x - mean) / std_dev
- Prevents features with larger ranges from dominating
- Required for distance-based algorithms

**Where used**: `backend/services/ml_service.py` - preprocessing must match training exactly

</details>

<details>
<summary><b>Step 2: Logistic Regression (Classification) - What, Why, How</b></summary>

**File Location**: `model/classification_model.pkl`

**What**: Binary classifier predicting Pass/Fail with probability scores

**Why Logistic Regression?**:
- Binary classification problem (Pass/Fail)
- Provides probability scores (confidence levels)
- Interpretable coefficients show feature importance
- Fast training and inference (<50ms)
- Works well with linearly separable data

**How it works**:
- Uses sigmoid function: P(y=1) = 1 / (1 + e^(-z))
- z = w1*x1 + w2*x2 + ... + wn*xn + b
- Outputs probability between 0 and 1
- Threshold at 0.5 for binary decision

**Training Code**:
```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

clf = LogisticRegression(max_iter=1000, random_state=42)
clf.fit(X_train_scaled, y_train_class)

y_pred = clf.predict(X_test_scaled)
y_proba = clf.predict_proba(X_test_scaled)

print(classification_report(y_test_class, y_pred))
```

**Performance Metrics**:
```
              precision    recall  f1-score   support
        Fail       0.98      0.99      0.99       963
        Pass       0.67      0.43      0.52        37
    accuracy                           0.97      1000
```

**What these metrics mean**:
- **Precision**: Of predicted Pass, 67% were actually Pass
- **Recall**: Of actual Pass, only 43% were caught (class imbalance issue)
- **Accuracy**: 97.1% overall (dominated by majority Fail class)

**Feature Importance** (Top 5 coefficients):
1. study_hours_per_day (+2.34) - More study hours increase pass probability
2. quiz_average_score (+1.89) - Higher quiz scores predict passing
3. mental_health_score (+1.56) - Better mental health helps
4. focus_index (+1.23) - Higher focus increases pass chance
5. social_media_hours (-1.12) - More social media decreases pass probability

**Where used**: `backend/services/ml_service.py` - `run_predictions()` function

**How used in production**:
```python
pred_class = int(models['classifier'].predict(scaled_df)[0])
proba = models['classifier'].predict_proba(scaled_df)[0]
pass_prob = round(float(proba[1]) * 100, 1)
fail_prob = round(float(proba[0]) * 100, 1)
```

</details>

<details>
<summary><b>Step 3: Linear Regression (Score Prediction) - What, Why, How</b></summary>

**File Location**: `model/regression_model.pkl`

**What**: Predicts continuous exam score (0-100 range)

**Why Linear Regression?**:
- Continuous output needed (not just Pass/Fail)
- Fast and interpretable
- Provides baseline for complex models
- Works when relationship between features and target is approximately linear

**How it works**:
- Fits line: y = w1*x1 + w2*x2 + ... + wn*xn + b
- Minimizes Mean Squared Error (MSE)
- Finds optimal weights (w) using gradient descent or closed-form solution
- Predicts by multiplying features with learned weights

**Training Code**:
```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

reg = LinearRegression()
reg.fit(X_train_scaled, y_train_reg)

y_pred_reg = reg.predict(X_test_scaled)
y_pred_reg = np.clip(y_pred_reg, 0, 100)  # Clip to valid range

print(f"R² Score: {r2_score(y_test_reg, y_pred_reg):.3f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test_reg, y_pred_reg)):.2f}")
print(f"MAE: {mean_absolute_error(y_test_reg, y_pred_reg):.2f}")
```

**Performance Metrics**:
- **R² Score: 0.85** - Model explains 85% of variance in exam scores
- **RMSE: 5.2 points** - Average error magnitude (root mean squared error)
- **MAE: 4.0 points** - Average absolute error

**What these metrics mean**:
- R² of 0.85 is strong (1.0 is perfect, 0.0 is random)
- Model predicts within ±5 points on average
- Good enough for early warning system

**Where used**: `backend/services/ml_service.py` - `run_predictions()` function

**How used in production**:
```python
pred_score = round(float(np.clip(models['regressor'].predict(scaled_df)[0], 0, 100)), 2)
grade = get_grade(pred_score)  # A/B/C/D/F based on score
```

</details>

<details>
<summary><b>Step 4: K-Means Clustering (Learner Profiling) - What, Why, How</b></summary>

**File Location**: `model/clustering_model.pkl`

**What**: Unsupervised learning algorithm that groups students into 4 behavioral archetypes

**Why K-Means Clustering?**:
- Unsupervised learning - discovers natural groupings without labels
- No labeled data needed for learner types
- Fast and scalable
- Provides interpretable student segments for personalized advice

**How it works**:
1. Initialize K random centroids (cluster centers)
2. Assign each point to nearest centroid
3. Recalculate centroids as mean of assigned points
4. Repeat steps 2-3 until convergence
5. Distance metric: Euclidean distance in scaled feature space

**Why K=4?**:
```python
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Elbow method to find optimal K
inertias = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
    kmeans.fit(X_train_scaled)
    inertias.append(kmeans.inertia_)

plt.plot(range(1, 11), inertias, 'bo-')
plt.xlabel('Number of Clusters')
plt.ylabel('Inertia (Within-cluster sum of squares)')
plt.show()
```

**Elbow method**: Plot shows "elbow" at K=4 where adding more clusters gives diminishing returns

**Training Code**:
```python
kmeans = KMeans(n_clusters=4, n_init=10, random_state=42)
kmeans.fit(X_train_scaled)

cluster_labels = {
    0: "High Achiever",
    1: "Average Learner",
    2: "Struggling Learner",
    3: "Developing Learner"
}
```

**Cluster Characteristics**:

1. **High Achiever** (~1,340 students)
   - High study hours (>6h/day)
   - Strong quiz scores (>75)
   - Low distractions (<2h social media)
   - Good sleep (7-9h)
   - Low burnout

2. **Average Learner** (~1,290 students)
   - Moderate study hours (3-5h/day)
   - Average scores (50-70)
   - Balanced lifestyle
   - Room for improvement

3. **Struggling Learner** (~1,220 students)
   - Low study hours (<3h/day)
   - High distractions (>4h social media)
   - Poor wellness indicators
   - High burnout
   - Low scores

4. **Developing Learner** (~1,135 students)
   - Improving trajectory
   - Mixed performance
   - Positive effort indicators
   - Needs consistency

**Where used**: `backend/services/ml_service.py` - `run_predictions()` function

**How used in production**:
```python
pred_cluster = int(models['kmeans'].predict(scaled_df)[0])
raw_ltype = models['cluster_label_map'].get(pred_cluster, "Unknown")
# Further refined based on score and pass probability
ltype = _resolve_learner_type(pred_score, pass_prob, raw_ltype)
```

</details>

<details>
<summary><b>Step 5: Model Serialization - What, Why, How</b></summary>

**What**: Save trained models to disk for later use in production

**Why**: 
- Train once, use many times
- Avoid retraining on every prediction
- Consistent model version across deployments
- Fast loading at runtime

**Files Created**:
- `model/classification_model.pkl` - Trained Logistic Regression
- `model/regression_model.pkl` - Trained Linear Regression  
- `model/clustering_model.pkl` - Trained K-Means
- `model/scaler.pkl` - Fitted StandardScaler (critical for preprocessing)
- `model/feature_columns.pkl` - Feature order for alignment
- `model/cluster_label_map.pkl` - Cluster ID to label mapping

**How**:
```python
import joblib

joblib.dump(clf, 'model/classification_model.pkl')
joblib.dump(reg, 'model/regression_model.pkl')
joblib.dump(kmeans, 'model/clustering_model.pkl')
joblib.dump(scaler, 'model/scaler.pkl')
joblib.dump(X.columns.tolist(), 'model/feature_columns.pkl')
joblib.dump(cluster_labels, 'model/cluster_label_map.pkl')
```

**Why Joblib?**:
- Efficient serialization for NumPy arrays
- Preserves model state exactly
- Fast loading (<100ms for all models)
- Standard in scikit-learn ecosystem
- Compression support

**Where loaded**: `backend/services/ml_service.py` - `load_models()` at startup

</details>

### Phase 3: Model Deployment and Inference

<details>
<summary><b>Backend ML Service - What, Why, How</b></summary>

**File Location**: `backend/services/ml_service.py`

**What**: Production ML inference service

**Why**: Centralized ML logic, fast predictions, consistent preprocessing

**Model Loading at Startup**:
```python
def load_models() -> dict:
    global _models
    try:
        _models['classifier'] = joblib.load(MODEL_DIR / "classification_model.pkl")
        _models['regressor'] = joblib.load(MODEL_DIR / "regression_model.pkl")
        _models['kmeans'] = joblib.load(MODEL_DIR / "clustering_model.pkl")
        _models['scaler'] = joblib.load(MODEL_DIR / "scaler.pkl")
        _models['feature_columns'] = joblib.load(MODEL_DIR / "feature_columns.pkl")
        _models['loaded'] = True
    except Exception as e:
        _models['loaded'] = False
        _models['error'] = str(e)
    return _models
```

**Why load at startup?**:
- Models loaded once into memory
- Avoids disk I/O on every prediction
- Faster inference (<50ms per prediction)
- Singleton pattern ensures consistency

**Preprocessing Pipeline**:
```python
def preprocess_input(raw: dict, models: dict):
    df = pd.DataFrame([raw])
    
    # Categorical encoding (MUST match training)
    df['gender'] = df['gender'].map({'Male': 1, 'Female': 0, 'Other': 2})
    
    # Feature engineering (MUST match training)
    df['total_active_hours'] = df['study_hours'] + df['self_study_hours'] + df['online_classes_hours']
    
    # Feature alignment (MUST match training order)
    cols = models['feature_columns']
    df = df[cols]
    
    # Scale features (using training statistics)
    scaled = models['scaler'].transform(df)
    return pd.DataFrame(scaled, columns=cols)
```

**Why exact replication?**:
- Preprocessing MUST match training exactly
- Feature order matters for model input
- Encoding must use same mappings
- Scaling uses training mean/std (not test data)
- Any mismatch causes incorrect predictions

**Prediction Function**:
```python
def run_predictions(raw: dict) -> dict:
    models = get_models()
    scaled_df = preprocess_input(raw, models)
    
    # Run all 3 models simultaneously
    pred_class = int(models['classifier'].predict(scaled_df)[0])
    proba = models['classifier'].predict_proba(scaled_df)[0]
    pred_score = round(float(np.clip(models['regressor'].predict(scaled_df)[0], 0, 100)), 2)
    pred_cluster = int(models['kmeans'].predict(scaled_df)[0])
    
    # Post-processing
    pass_prob = round(float(proba[1]) * 100, 1)
    learner_type = _resolve_learner_type(pred_score, pass_prob, cluster_label)
    
    return {
        "predicted_score": pred_score,
        "pass_probability": pass_prob,
        "classification": "Pass" if pred_class == 1 else "Fail",
        "learner_type": learner_type
    }
```

**Why run all 3 models?**:
- Provides comprehensive student profile
- Score + classification + archetype = complete picture
- Models complement each other
- Total inference time <50ms (parallel execution)

**Where called**: `backend/routes/predict.py` - POST /predict endpoint

</details>

---

## AI and LLM Integration - Complete Workflow

### Phase 1: RAG (Retrieval-Augmented Generation) System


<details>
<summary><b>What is RAG and Why Use It?</b></summary>

**What**: RAG (Retrieval-Augmented Generation) combines information retrieval with LLM generation

**Why**: 
- LLMs have knowledge cutoff dates
- Cannot access domain-specific information
- May hallucinate facts
- No control over knowledge base

**How RAG solves this**:
1. Retrieve relevant documents from vector database
2. Inject retrieved context into LLM prompt
3. LLM generates response grounded in retrieved facts
4. Reduces hallucination, increases accuracy

**Where used in AcadIQ**: Study Coach retrieves relevant study resources before generating advice

</details>

<details>
<summary><b>Vector Database - ChromaDB Setup - What, Why, How</b></summary>

**File Location**: `backend/services/rag_service.py`

**What**: Vector database storing study resource embeddings for semantic search

**Why ChromaDB?**:
- Open-source vector database
- Lightweight (no separate server needed)
- Fast similarity search (<100ms)
- Persistent storage on disk
- Easy integration with LangChain

**Step 1: Resource Collection**

**File**: `backend/data/resources.json`

```json
[
  {
    "topic": "Time Management",
    "title": "Pomodoro Technique",
    "description": "25-minute focused work sessions with 5-minute breaks",
    "url": "https://example.com/pomodoro"
  }
]
```

**Why JSON format?**: Easy to maintain, structured data, version controlled, simple to parse

**Step 2: Text Embedding**

```python
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
```

**What are embeddings?**:
- Convert text to dense vector representations (384 dimensions)
- Similar texts have similar vectors (cosine similarity)
- Enables semantic search (meaning-based, not keyword-based)

**Why sentence-transformers/all-MiniLM-L6-v2?**:
- Lightweight (80MB model)
- Fast inference (<10ms per document)
- Good balance of speed and quality
- Optimized for semantic similarity tasks
- 384-dimensional vectors

**How embeddings work**:
- Neural network trained on sentence pairs
- Learns to map similar sentences to nearby vectors
- "improve focus" and "increase concentration" have similar embeddings
- Distance metric: cosine similarity

**Step 3: Vector Store Creation**

```python
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

documents = []
for resource in resources:
    doc = Document(
        page_content=f"{resource['topic']}: {resource['description']}",
        metadata={
            "topic": resource["topic"],
            "title": resource["title"],
            "url": resource["url"]
        }
    )
    documents.append(doc)

vector_store = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory="backend/chroma_db",
    collection_name="acadiq_resources"
)
```

**What happens here**:
1. Each resource converted to Document object
2. Text embedded to 384-dim vector
3. Vector + metadata stored in ChromaDB
4. Persisted to disk for reuse

**Step 4: Semantic Search**

```python
def retrieve_resources(query: str, k: int = 3) -> list[dict]:
    results = vector_store.similarity_search(query, k=k)
    return [
        {
            "topic": doc.metadata["topic"],
            "title": doc.metadata["title"],
            "url": doc.metadata["url"]
        }
        for doc in results
    ]
```

**How similarity search works**:
1. Query text embedded to vector
2. Compute cosine similarity with all stored vectors
3. Return top-k most similar documents
4. Metadata extracted and returned

**Example**:
- Query: "How to improve focus while studying?"
- Embedded to vector
- Finds similar vectors: Pomodoro Technique, Deep Work, Distraction Management
- Returns top 3 resources

**Where used**: `backend/services/coach_service.py` - `generate_plan()` function

</details>

### Phase 2: LLM Integration with LangChain

<details>
<summary><b>What is LangChain and Why Use It?</b></summary>

**What**: Framework for building LLM-powered applications

**Why LangChain?**:
- Abstracts LLM API calls
- Manages conversation history
- Integrates with vector databases
- Provides prompt templates
- Handles streaming responses
- Vendor-agnostic (easy to switch LLMs)

**Key Components Used**:
1. ChatGroq - LLM interface
2. Messages - SystemMessage, HumanMessage, AIMessage
3. Vector store integration
4. Memory management

**Where used**: All AI coach functionality in `backend/services/coach_service.py`

</details>

<details>
<summary><b>LLM Provider - Groq API - What, Why, How</b></summary>

**File Location**: `backend/services/coach_service.py`

**What**: LLM inference platform hosting Llama 3.3 70B

**Setup**:
```python
from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    groq_api_key=os.getenv("GROQ_API_KEY")
)
```

**Why Groq?**:
- Ultra-fast inference (300+ tokens/second)
- 10x faster than standard APIs
- Cost-effective
- Low latency (2-4 seconds for full response)
- Free tier available

**Why Llama 3.3 70B?**:
- 70 billion parameters (high quality)
- State-of-the-art open model
- Strong reasoning capabilities
- Good at following instructions
- Multilingual support
- Open-source (no vendor lock-in)

**Why temperature=0.7?**:
- Controls randomness in generation
- 0.0 = deterministic (same output every time)
- 1.0 = maximum creativity/randomness
- 0.7 = balanced (creative but consistent)
- Good for conversational AI

**How LLM works**:
- Transformer architecture with attention mechanism
- Predicts next token based on previous tokens
- Trained on massive text corpus
- Fine-tuned for instruction following

**Where used**: All AI coach interactions

</details>

<details>
<summary><b>Conversation Memory Management - What, Why, How</b></summary>

**File Location**: `backend/services/coach_service.py`

**What**: Stores conversation history for multi-turn dialogues

**Implementation**:
```python
# In-memory session store
_sessions: Dict[str, List] = {}

def get_or_create_session(user_email: str) -> List:
    if user_email not in _sessions:
        _sessions[user_email] = []
    return _sessions[user_email]

def chat(user_email: str, message: str, student_profile: dict) -> str:
    history = get_or_create_session(user_email)
    
    system_msg = _build_system_message(student_profile)
    messages = [system_msg] + history + [HumanMessage(content=message)]
    
    response = llm.invoke(messages)
    reply = response.content
    
    # Save to memory
    history.append(HumanMessage(content=message))
    history.append(AIMessage(content=reply))
    
    return reply
```

**Why conversation memory?**:
- Enables multi-turn conversations
- LLM sees full conversation history
- Maintains context across messages
- More natural dialogue

**Why in-memory storage?**:
- Fast access (<1ms)
- No database overhead
- Suitable for short sessions
- Cleared on server restart (privacy)

**Message Types**:
1. **SystemMessage**: Instructions for LLM behavior
2. **HumanMessage**: User input
3. **AIMessage**: LLM response

**How it works**:
1. User sends message
2. Retrieve conversation history for user
3. Prepend system message with student profile
4. Append new user message
5. Send all messages to LLM
6. Store LLM response in history
7. Return response to user

**Example Conversation Flow**:
```
System: You are AcadIQ Coach. Student score: 74/100...
Human: What are my weaknesses?
AI: Based on your profile, your top weaknesses are sleep (5.5h vs 7.2h avg)...
Human: How can I improve sleep?
AI: Given your current 5.5 hours (you mentioned earlier), try...
```

**Where used**: `backend/routes/coach.py` - POST /coach/chat endpoint

</details>

<details>
<summary><b>Prompt Engineering - System Prompt - What, Why, How</b></summary>

**File Location**: `backend/services/coach_service.py`

**What**: Carefully crafted instructions that guide LLM behavior

**System Prompt Template**:
```python
COACH_SYSTEM_PROMPT_TEMPLATE = """You are AcadIQ Coach — a study assistant and academic mentor. 

You answer questions related to studying, academics, exam preparation, student wellness (including mental health, focus, burnout, sleep), learning resources, study plans, and the student's AcadIQ profile, strengths, and weaknesses. 

You MUST REFUSE any request that involves illegal activities, harmful or violent content, or tasks completely unrelated to the student life. 

If asked anything far outside your scope, respond ONLY with: "I am your study coach and I can only help with academic topics. Is there anything about your studies I can help with?"

Here is the student's profile from their ML analysis:
- Predicted Exam Score: {student_score}/100
- Classification: {classification} (Pass Probability: {pass_probability}%)
- Learner Archetype: {learner_type}
- Top Weaknesses Identified: {top_weaknesses}

Your role:
1. Be warm, encouraging, and specific — never generic
2. Reference the student's actual numbers when giving advice
3. Ask follow-up questions to understand their situation better
4. Give actionable, concrete steps — not vague advice
5. Think step by step before answering (chain-of-thought)
6. Keep responses concise — 3 to 5 sentences max per reply unless generating a plan"""
```

**Why prompt engineering?**:
- Critical for consistent, high-quality outputs
- Defines personality, constraints, and capabilities
- Prevents off-topic or harmful responses
- Enables personalization

**Key Components**:
1. **Role Definition**: "You are AcadIQ Coach"
2. **Scope Boundaries**: "MUST REFUSE... unrelated to student life"
3. **Safety Guardrails**: Explicit refusal instructions
4. **Context Injection**: Student profile data from ML models
5. **Behavioral Guidelines**: 5 specific rules
6. **Output Format**: "3 to 5 sentences max"

**Why include student profile?**:
- Enables personalized responses
- LLM references actual numbers
- Grounds advice in student's reality
- Prevents generic responses

**Why chain-of-thought?**:
- Improves reasoning quality
- Reduces errors
- More logical responses
- Better problem-solving

**Where used**: Every AI coach interaction

</details>

<details>
<summary><b>RAG-Enhanced Study Plan Generation - What, Why, How</b></summary>

**File Location**: `backend/services/coach_service.py`

**What**: Combines ML predictions + RAG retrieval + LLM generation for personalized study plans

**Function**: `generate_plan(student_profile, resources)`

**Step 1: Retrieve Relevant Resources**
```python
# In backend/routes/coach.py
from services.rag_service import retrieve_resources

weaknesses = [w['feature'] for w in student_profile['top_weaknesses']]
query = f"study techniques for {', '.join(weaknesses)}"

resources = retrieve_resources(query, k=3)
```

**Why retrieve first?**: Ground LLM generation in factual study resources

**Step 2: Build Prompt with Retrieved Context**
```python
def generate_plan(student_profile: dict, resources: list[dict]) -> dict:
    weaknesses_str = _format_weaknesses(student_profile['top_weaknesses'])
    
    resources_text = "\n".join([
        f"- {r['title']}: {r['description']} ({r['url']})"
        for r in resources
    ])
    
    prompt = f"""Generate a personalized 7-day study plan for this student.

Student Profile:
- Predicted Score: {student_profile['predicted_score']}/100
- Classification: {student_profile['classification']}
- Pass Probability: {student_profile['pass_probability']}%
- Learner Type: {student_profile['learner_type']}
- Top Weaknesses: {weaknesses_str}

Available Resources:
{resources_text}

Format the plan EXACTLY as:
Day 1: [Focus Area] — [Specific Task] — [Time]
Day 2: [Focus Area] — [Specific Task] — [Time]
...
Weekly Goal: [One measurable goal]"""
    
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"plan": response.content}
```

**How RAG enhances generation**:
1. ML model identifies weaknesses (e.g., sleep_hours: 5.5 vs 7.2 avg)
2. Semantic search finds relevant resources (Sleep Hygiene Guide)
3. Resources injected into prompt
4. LLM generates plan using retrieved knowledge
5. Plan references specific techniques from resources

**Example Flow**:
- Weakness: "sleep_hours (5.5 vs avg 7.2)"
- Query: "study techniques for sleep_hours"
- Retrieved: "Sleep Hygiene Guide", "Circadian Rhythm Optimization"
- Generated Plan: "Day 1: Sleep Optimization — Establish 10 PM bedtime routine — 30 min"

**Why this approach?**:
- Grounds plan in evidence-based techniques
- Provides actionable resources with URLs
- Reduces hallucination
- Ensures quality recommendations
- Combines ML insights with LLM generation

**Where used**: `backend/routes/coach.py` - POST /coach/plan endpoint

</details>

<details>
<summary><b>AI Safety and Guardrails - What, Why, How</b></summary>

**File Location**: `backend/routes/coach.py`

**What**: Multi-layer defense system to prevent misuse

**Why needed?**:
- LLMs can generate harmful content
- Users may try off-topic or malicious queries
- Need to protect users and prevent abuse
- Reduce API costs from spam

**Layer 1: System Prompt Guardrails**
```python
"You MUST REFUSE any request that involves illegal activities, harmful or violent content, or tasks completely unrelated to the student life."
```

**Why**: First line of defense, guides LLM behavior

**Layer 2: Input Keyword Filter**
```python
BLOCKED_KEYWORDS = [
    'hack', 'cheat', 'steal', 'illegal', 'weapon', 
    'drug', 'violence', 'harm', 'suicide'
]

def check_input_safety(message: str) -> bool:
    message_lower = message.lower()
    for keyword in BLOCKED_KEYWORDS:
        if keyword in message_lower:
            return False
    return True
```

**Why**: Catches obvious misuse before calling expensive LLM API

**Layer 3: Topic Relevance Check**
```python
ACADEMIC_TOPICS = [
    'study', 'exam', 'learning', 'focus', 'memory',
    'sleep', 'stress', 'burnout', 'time management'
]

def is_academic_topic(message: str) -> bool:
    message_lower = message.lower()
    return any(topic in message_lower for topic in ACADEMIC_TOPICS)
```

**Why**: Warns users when going off-topic

**Layer 4: Rate Limiting**
```python
from collections import defaultdict
import time

_rate_limit_store = defaultdict(list)
MAX_REQUESTS_PER_HOUR = 20

def check_rate_limit(user_email: str):
    now = time.time()
    hour_ago = now - 3600
    
    _rate_limit_store[user_email] = [
        t for t in _rate_limit_store[user_email] if t > hour_ago
    ]
    
    if len(_rate_limit_store[user_email]) >= MAX_REQUESTS_PER_HOUR:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    _rate_limit_store[user_email].append(now)
```

**Why**: Prevents abuse, reduces costs, ensures fair usage

**Why multiple layers?**:
- Defense in depth
- Catches different types of misuse
- Redundancy if one layer fails
- Comprehensive protection

**Where used**: All AI coach endpoints

</details>

### Phase 3: Quiz Generation with Structured Output

<details>
<summary><b>LLM JSON Mode for Structured Generation - What, Why, How</b></summary>

**File Location**: `backend/services/quiz_service.py`

**What**: Generate structured quiz data using LLM

**Challenge**: LLMs generate free-form text, but we need structured quiz data (questions, options, answers)

**Solution**: JSON mode + schema validation

**Implementation**:
```python
def generate_quiz(topic: str, count: int, level: str, difficulty: str) -> dict:
    prompt = f"""Generate a quiz on "{topic}" with {count} questions.
    
Academic Level: {level}
Difficulty: {difficulty}

Output MUST be valid JSON with this exact structure:
{{
  "title": "Quiz title",
  "questions": [
    {{
      "number": 1,
      "question": "Question text?",
      "options": [
        {{"label": "A", "text": "Option A"}},
        {{"label": "B", "text": "Option B"}}
      ],
      "correct_option_label": "A",
      "explanation": "Why A is correct"
    }}
  ]
}}"""
    
    response = llm.invoke([HumanMessage(content=prompt)])
    quiz_data = json.loads(response.content)
    
    # Validate with Pydantic
    validated = QuizGenerateResponse(**quiz_data)
    return validated.dict()
```

**Why JSON mode?**:
- Ensures parseable output
- Enables frontend rendering
- Type-safe data structures
- Prevents malformed responses

**Why Pydantic validation?**:
- Runtime type checking
- Automatic data validation
- Clear error messages if structure wrong
- Schema documentation

**How it works**:
1. Prompt explicitly requests JSON format
2. LLM generates JSON string
3. Parse JSON to Python dict
4. Validate with Pydantic schema
5. Return validated data

**Where used**: `backend/routes/quiz.py` - POST /quiz/generate endpoint

</details>

---

## Complete System Architecture

<details>
<summary><b>Data Flow Diagram - End to End</b></summary>

```
User Input (Frontend)
    |
    v
[React Form Validation]
    |
    v
[Axios HTTP Client + JWT Token]
    |
    v
[FastAPI Backend]
    |
    +---> [Authentication Middleware - JWT Verification]
    |
    +---> [Pydantic Validation - Type Checking]
    |
    v
[ML Service]
    |
    +---> Load Models from disk (joblib)
    +---> Preprocess Input (encoding, feature engineering, scaling)
    +---> Run 3 Models in Parallel
    |     - Logistic Regression (Pass/Fail)
    |     - Linear Regression (Score 0-100)
    |     - K-Means (Learner Type)
    +---> Post-process Results (probabilities, grade, recommendations)
    |
    v
[MongoDB]
    |
    +---> Save Prediction Report
    +---> Link to User Account
    +---> Store Input Data for History
    |
    v
[Response to Frontend]
    |
    v
[Results Dashboard]
    |
    +---> Animated Score Ring (CSS animations)
    +---> Radar Chart (Recharts library)
    +---> Recommendations Grid
    +---> Download PDF/Badge (jsPDF, Canvas API)
    |
    v
[AI Coach (Optional)]
    |
    +---> RAG Retrieval (ChromaDB semantic search)
    +---> LLM Generation (Groq API - Llama 3.3 70B)
    +---> Session Memory (in-memory store)
    +---> Streaming Response
```

</details>

<details>
<summary><b>Backend Architecture - FastAPI Application</b></summary>

**File Location**: `backend/main.py`

**What**: Async Python web framework serving ML and AI endpoints

**Application Lifecycle**:
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("[Startup] Loading ML models...")
    ml_service.load_models()
    print("[Startup] Initializing RAG vector store...")
    rag_service.initialize_vector_store()
    print("[Startup] Ready.")
    yield
    # Shutdown (nothing to clean up)

app = FastAPI(
    title="AcadIQ API",
    version="2.0.0",
    lifespan=lifespan
)
```

**Why lifespan events?**:
- Load heavy resources once at startup
- Avoid repeated disk I/O
- Faster request handling
- Clean shutdown if needed

**CORS Configuration**:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
```

**Why CORS?**: Frontend and backend on different domains, browser security requires explicit permission

**API Routes**:
- `/auth/*` - Authentication (register, login, get user)
- `/predict/*` - ML predictions (predict, history)
- `/coach/*` - AI coach (chat, diagnose, plan, reset)
- `/quiz/*` - Quiz generation
- `/` - Health check
- `/health` - Models loaded status

</details>

<details>
<summary><b>Frontend Architecture - React Application</b></summary>

**File Location**: `frontend/src/App.jsx`

**What**: Single-page application with client-side routing

**React Router Setup**:
```javascript
<BrowserRouter>
  <AuthProvider>
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/auth" element={<Auth />} />
      <Route path="/input" element={<ProtectedRoute><InputForm /></ProtectedRoute>} />
      <Route path="/results" element={<ProtectedRoute><Results /></ProtectedRoute>} />
      <Route path="/coach" element={<ProtectedRoute><StudyCoach /></ProtectedRoute>} />
      <Route path="/quiz" element={<ProtectedRoute><QuizBot /></ProtectedRoute>} />
      <Route path="/history" element={<ProtectedRoute><History /></ProtectedRoute>} />
    </Routes>
  </AuthProvider>
</BrowserRouter>
```

**Why React Router?**: Client-side routing (no page reloads), protected routes for authentication

**Authentication Context**:
```javascript
// File: frontend/src/context/AuthContext.jsx
const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const stored = localStorage.getItem('acadiq_user')
    return stored ? JSON.parse(stored) : null
  })
  
  const [token, setToken] = useState(() => 
    localStorage.getItem('acadiq_token')
  )
  
  const login = (jwtToken, userData) => {
    setToken(jwtToken)
    setUser(userData)
    localStorage.setItem('acadiq_token', jwtToken)
    localStorage.setItem('acadiq_user', JSON.stringify(userData))
  }
  
  return (
    <AuthContext.Provider value={{ user, token, login, logout, isAuthenticated: !!token }}>
      {children}
    </AuthContext.Provider>
  )
}
```

**Why Context API?**: Global state management, avoid prop drilling, persistent authentication

**API Client with JWT**:
```javascript
// File: frontend/src/api/client.js
import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000'
})

// Automatic JWT injection
apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('acadiq_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const predictAPI = {
  predict: (data) => apiClient.post('/predict', data),
  getHistory: () => apiClient.get('/predict/history')
}
```

**Why Axios interceptors?**: Automatic token injection, no manual header management, centralized error handling

</details>

<details>
<summary><b>Database Schema - MongoDB Collections</b></summary>

**File Location**: `backend/database/mongo.py`

**What**: NoSQL database storing users and prediction reports

**Why MongoDB?**:
- Flexible schema (easy to add fields)
- JSON-like documents (matches API responses)
- Fast queries with indexes
- Cloud-hosted (MongoDB Atlas)
- Free tier available

**Users Collection**:
```javascript
{
  _id: ObjectId("..."),
  name: "John Doe",
  email: "john@example.com",
  password_hash: "pbkdf2:sha256:...",  // PBKDF2-SHA256 hashing
  created_at: ISODate("2024-01-15T10:30:00Z")
}
```

**Indexes**: `email` (unique index for fast lookup and uniqueness constraint)

**Reports Collection**:
```javascript
{
  _id: ObjectId("..."),
  user_email: "john@example.com",
  timestamp: "2024-01-15T10:35:00Z",
  prediction: {
    predicted_score: 74.5,
    grade: "B",
    pass_probability: 84.2,
    fail_probability: 15.8,
    classification: "Pass",
    learner_type: "High Achiever",
    cluster_id: 0,
    top_weaknesses: [...],
    recommendations: [...]
  },
  input_data: {
    age: 20,
    gender: "Male",
    study_hours: 4.0,
    // ... all 23 input features
  }
}
```

**Indexes**: 
- `user_email` (for fast user history queries)
- `timestamp` (for chronological sorting)

</details>

---

## Quick Start Guide

<details>
<summary><b>Installation Steps</b></summary>

**Prerequisites**:
- Python 3.9+
- Node.js 18+
- MongoDB Atlas account (free tier)
- Groq API key (free tier)

**Step 1: Clone Repository**
```bash
git clone https://github.com/anand-242003/AcadQ-2.git
cd AcadQ-2
```

**Step 2: Backend Setup**
```bash
python3 -m venv .venv
source .venv/bin/activate
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
```

**Step 3: Frontend Setup**
```bash
cd ../frontend
npm install
cp .env.example .env
# Default: VITE_API_URL=http://localhost:8000
```

**Step 4: Run Application**

Terminal 1 - Backend:
```bash
cd backend
source ../.venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

Open: http://localhost:5173

</details>

---

## Performance Metrics

### Model Performance

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Classification Accuracy | 97.1% | High overall accuracy |
| Pass Class Recall | 43% | Needs improvement (class imbalance) |
| Regression R² | 0.85 | Explains 85% of variance |
| Regression RMSE | 5.2 | Average error ±5.2 points |
| Clustering K | 4 | Optimal via elbow method |

### System Performance

| Metric | Value |
|--------|-------|
| API Response Time | <200ms (avg) |
| ML Prediction Time | <50ms |
| LLM Response Time | 2-4s (Groq) |
| RAG Retrieval Time | <100ms |
| Frontend Load Time | <2s (initial) |

---

## Team

| Name | Role |
|---|---|
| Rajdeep Sanyal | ML Lead and Project Coordinator |
| Rajat Srivastava | Data Engineering and EDA |
| Anand Mishra | Clustering and Visualization |
| Omved Nagre | Application Development and Deployment |

---

## Acknowledgments

- scikit-learn - ML models
- LangChain - LLM orchestration
- Groq - Fast LLM inference
- MongoDB Atlas - Database hosting
- Vercel & Render - Deployment platforms
- React & FastAPI - Framework foundations
