# AcadIQ -- Intelligent Learning Analytics and Agentic AI Study Coach

**Milestone 1: ML-Based Learning Analytics System**

AcadIQ is a machine learning pipeline and web application that predicts student academic performance, classifies learners into behavioral archetypes, and generates personalized study recommendations. This repository contains the Milestone 1 implementation: a classical ML analytics system built on top of student behavioral, wellness, and academic performance data.

Milestone 2 (in progress) will extend this into a full agentic AI study coach using LangGraph, RAG-based resource retrieval, and session-based memory.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [ML Pipeline](#ml-pipeline)
  - [Models](#models)
  - [Dataset](#dataset)
  - [Preprocessing](#preprocessing)
- [Model Performance](#model-performance)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Notebook](#running-the-notebook)
- [Application](#application)
  - [Input Features](#input-features)
  - [Output Predictions](#output-predictions)
- [Known Limitations](#known-limitations)
- [Roadmap](#roadmap)
- [Team](#team)
- [License](#license)

---

## Project Overview

AcadIQ addresses the early identification of at-risk students using behavioral and academic trace data collected before final examinations. The system produces three simultaneous outputs from a single prediction pass:

- A continuous exam score estimate (0 to 100) via Linear Regression
- A binary Pass/Fail classification with confidence probabilities via Logistic Regression
- A learner archetype assignment (High Achiever, Average, Struggling, Developing) via K-Means clustering

These outputs are served through a deployed web frontend that accepts 20+ input features and returns a full performance report with a radar chart profile and rule-based recommendations.

---

## Architecture

```
StudentData.csv
      |
      v
+------------------+
|   Preprocessing  |  -- missing value imputation, StandardScaler, stratified split
+------------------+
      |
      +---------------------------+---------------------------+
      |                           |                           |
      v                           v                           v
+-------------+          +----------------+         +------------------+
|  Logistic   |          |    Linear      |         |     K-Means      |
|  Regression |          |   Regression   |         |   Clustering     |
| (Pass/Fail) |          | (Exam Score)   |         | (Learner Type)   |
+-------------+          +----------------+         +------------------+
      |                           |                           |
      v                           v                           v
 Binary label              Continuous score          Cluster assignment
 + probability             (0-100 range)             (4 archetypes)
      |                           |                           |
      +---------------------------+---------------------------+
                                  |
                                  v
                      +----------------------+
                      |  AcadIQ Web Frontend |
                      |  React.js + REST API |
                      +----------------------+
                                  |
                                  v
                      Performance Report Page
                      (Score, Class, Archetype,
                       Radar Chart, Recommendations)
```

---

## ML Pipeline

### Models

| Model | Task | Algorithm | Library |
|---|---|---|---|
| Classifier | Pass/Fail prediction | Logistic Regression | scikit-learn |
| Regressor | Exam score prediction | Linear Regression | scikit-learn |
| Clustering | Learner profiling | K-Means (K=4) | scikit-learn |

All three models are trained in `GENAICAPSTONE.ipynb`. Cluster count K=4 was selected via the elbow method (inertia computed for K=1 to K=10, n_init=10). PCA (2 components) is applied post-clustering for visualization only and does not affect the model used for inference.

### Dataset

The training dataset is `StudentData.csv`, a tabular file with approximately 5,000 student records. Features span five domains:

- **Academic performance** -- quiz scores, assignment scores, midterm score
- **Time and engagement** -- study hours per day, self-study hours, online class hours, topics completed
- **Wellness and lifestyle** -- sleep hours per night, mental health score, exercise minutes per day, caffeine intake
- **Behavioral indicators** -- social media hours, gaming hours, total screen time, focus index, productivity score, burnout level
- **Contextual variables** -- age, gender, academic level, part-time job status, upcoming deadline flag, internet quality

Target variables:

- `y_class`: binary label (0 = Fail, 1 = Pass) for Logistic Regression
- `y_reg`: continuous exam score for Linear Regression

### Preprocessing

The preprocessing pipeline applies the following transformations in order:

1. **Missing value treatment** -- column-wise mean imputation for all numerical features
2. **Feature scaling** -- `StandardScaler` fitted on the training partition only; applied to both train and test
3. **Stratified train/test split** -- 80/20 ratio, `random_state=42`, stratified on `y_class` to preserve class proportions
4. **Target construction** -- `y_class` and `y_reg` extracted from the raw dataframe after cleaning
5. **Clustering input** -- scaled feature matrix `X_scaled` passed directly to K-Means; PCA applied to `X_scaled` for visualization

> Note: In the current implementation, StandardScaler is fitted before the train/test split in some cells. A fully encapsulated `sklearn.pipeline.Pipeline` wrapping imputation and scaling is planned for Milestone 2 to eliminate any risk of leakage.

---

## Model Performance

### Logistic Regression (Classification)

Evaluated on the held-out test set (n = 1,000).

```
              precision    recall  f1-score   support

        Fail       0.98      0.99      0.99       963
        Pass       0.67      0.43      0.52        37

    accuracy                           0.97      1000
   macro avg       0.82      0.71      0.75      1000
weighted avg       0.97      0.97      0.97      1000

Overall Accuracy: 97.10%
```

**Confusion matrix values:**

```
                 Predicted Fail    Predicted Pass
  Actual Fail         955                8
  Actual Pass          21               16
```

**Interpretation:** The 97.10% accuracy figure is dominated by the majority Fail class (963 of 1000 test samples). The Pass class recall of 0.43 is the critical metric -- 21 of 37 actual Pass students are misclassified as Fail. This is a direct consequence of the 26:1 class imbalance in the dataset and is the primary target for improvement in the next iteration.

### Linear Regression (Score Prediction)

| Metric | Value |
|---|---|
| R-squared | ~0.85 |
| RMSE | ~5.2 score points |
| MAE | ~4.0 score points |

The model explains approximately 85% of variance in exam scores. Residual analysis reveals heteroscedasticity in the low-score range, where predictions cluster near zero due to a floor effect.

### K-Means Clustering

| Cluster Label | Approx. Count | Characteristics |
|---|---|---|
| High Achiever | ~1,340 | High study hours, strong quiz scores, low distraction |
| Average | ~1,290 | Moderate engagement, balanced lifestyle metrics |
| Struggling | ~1,220 | Low study hours, high distractions, lower wellness |
| Developing | ~1,135 | Mixed performance with positive effort indicators |

K=4 selected based on elbow method inflection. Cluster separation validated via PCA 2D projection.

### Feature Importance (Logistic Regression)

Top features by absolute coefficient magnitude:

```
1. study_hours_per_day
2. quiz_average_score
3. mental_health_score
4. focus_index
5. social_media_hours
6. sleep_hours
7. productivity_score
8. burnout_level
```

---

## Repository Structure

```
acadiq/
|
+-- GENAICAPSTONE.ipynb        # Main notebook: preprocessing, training, evaluation
+-- StudentData.csv            # Training dataset
+-- README.md                  # This file
|
+-- app/                       # Web application source
|   +-- src/
|   |   +-- components/        # React components (InputForm, ResultsPage, RadarChart)
|   |   +-- pages/             # Overview, InputData, Results
|   |   +-- utils/             # API client, feature normalization helpers
|   +-- public/
|   +-- package.json
|
+-- models/                    # Serialized model artifacts (if exported)
|   +-- logistic_model.pkl
|   +-- linear_model.pkl
|   +-- kmeans_model.pkl
|   +-- scaler.pkl
|
+-- docs/
    +-- AcadIQ_Milestone1_Report.docx   # Full technical report
```

---

## Getting Started

### Prerequisites

- Python 3.9 or higher
- pip
- Node.js 18 or higher (for the frontend only)
- A Google account (if running on Google Colab)

Python dependencies used in the notebook:

```
pandas
numpy
scikit-learn
matplotlib
seaborn
jupyter
```

### Installation

Clone the repository:

```bash
git clone https://github.com/<your-org>/acadiq.git
cd acadiq
```

Create a virtual environment and install Python dependencies:

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install pandas numpy scikit-learn matplotlib seaborn jupyter
```

Install frontend dependencies (optional, for local app development):

```bash
cd app
npm install
```

### Running the Notebook

Start Jupyter locally:

```bash
jupyter notebook GENAICAPSTONE.ipynb
```

Or open directly in Google Colab by uploading `GENAICAPSTONE.ipynb` and `StudentData.csv` to your Drive, then mounting Drive at the top of the notebook:

```python
from google.colab import drive
drive.mount('/content/drive')
```

Update the data path in the data loading cell to point to your mounted Drive path.

**Notebook cell order:**

1. Imports and configuration
2. Data loading and inspection (`df.head()`, `df.describe()`, null checks)
3. EDA -- distribution plots, class balance, correlation heatmap
4. Preprocessing -- imputation, scaling, train/test split, target construction
5. Logistic Regression -- training, evaluation, confusion matrix, feature importance
6. Linear Regression -- training, evaluation, actual vs predicted plot, residual plot
7. K-Means clustering -- elbow method, model fitting, archetype labeling, PCA visualization

Run all cells in order. Each cell prints its output inline.

---

## Application

The AcadIQ frontend is a React.js single-page application with three views:

- **Overview** -- Introduction, system stats, feature descriptions, three-step workflow
- **Input Data** -- 20+ feature sliders organized into five sections with a live summary panel that updates on each input change
- **Results** -- Full prediction report: predicted score, Pass/Fail probabilities, learner archetype, radar chart comparing user profile against student average, and four generated recommendations

### Input Features

The input form maps directly to the model feature matrix. Fields are organized as follows:

**Personal Information**
- Age (slider)
- Gender (dropdown: Male / Female / Other)
- Academic Level (dropdown: High School / Undergraduate / Postgraduate)
- Part-time Job (radio: Yes / No)
- Upcoming Deadline (radio: Yes / No)
- Internet Quality (dropdown: Poor / Average / Good / Excellent)

**Study Habits**
- Study Hours / Day
- Self-Study Hours / Day
- Online Class Hours / Day

**Screen and Distractions**
- Social Media Hours / Day
- Gaming Hours / Day
- Total Screen Time / Day

**Lifestyle**
- Sleep Hours / Night
- Exercise (min / day)
- Caffeine Intake (mg / day)

**Wellbeing and Scores**
- Mental Health Score (1 to 10)
- Focus Index (0 to 100)
- Burnout Level (0 to 100)
- Productivity Score (0 to 100)

### Output Predictions

All three model outputs are returned in a single prediction call:

```json
{
  "predicted_score": 31.41,
  "grade": "D",
  "pass_probability": 0.026,
  "fail_probability": 0.974,
  "classification": "Fail",
  "cluster_id": 1,
  "learner_type": "High Achiever",
  "recommendations": [
    {
      "category": "AT RISK",
      "text": "You are at risk of failing. Increase daily study hours significantly."
    },
    {
      "category": "PLANNING",
      "text": "Build a structured weekly timetable and commit to it every day."
    },
    {
      "category": "DISTRACTIONS",
      "text": "Aim to keep social media and gaming under 2 hours per day."
    },
    {
      "category": "LEARNER PROFILE",
      "text": "Consider mentoring peers. Teaching material is one of the most effective ways to master it."
    }
  ]
}
```

---

## Known Limitations

**Class imbalance (critical)**

The training dataset has a 26:1 Fail-to-Pass ratio (4963 Fail vs 187 Pass across the full dataset). The classifier achieves 97.10% overall accuracy but only 0.43 recall on the Pass class. Without intervention, the model misclassifies the majority of actual Pass students as Fail. Planned fixes: SMOTE on the training partition, `class_weight='balanced'` in LogisticRegression, and decision threshold tuning via the precision-recall curve.

**No cross-validation**

Current evaluation uses a single stratified 80/20 split. Performance estimates may be sensitive to `random_state`. Stratified k-fold (k=5 or k=10) is planned to produce mean and standard deviation estimates across folds.

**Linear model for non-linear score prediction**

Residual analysis shows heteroscedasticity in the low-score range. A polynomial feature expansion or Random Forest Regressor is expected to improve prediction in this region.

**No silhouette evaluation for clustering**

Cluster quality was assessed only via the elbow method (inertia). Silhouette score and Davies-Bouldin index for K=2 to K=10 have not been computed. The K=4 selection is visually validated via PCA but not quantitatively optimized.

**Preprocessing pipeline encapsulation**

The StandardScaler is currently fitted prior to the train/test split in some cells. A fully encapsulated `sklearn.pipeline.Pipeline` will be introduced in Milestone 2 to enforce strict train-only fitting during cross-validation.

---

## Roadmap

**Milestone 1 (current)**

- [x] Data preprocessing pipeline (imputation, scaling, stratified split)
- [x] Logistic Regression classifier with classification report and confusion matrix
- [x] Linear Regression regressor with RMSE, MAE, R-squared evaluation
- [x] K-Means clustering with elbow method and PCA visualization
- [x] Feature importance extraction from Logistic Regression coefficients
- [x] React frontend with input form, live summary, radar chart, and results page
- [x] Public deployment

**Milestone 2 (planned)**

- [ ] Class imbalance correction via SMOTE and class_weight balancing
- [ ] Ensemble model benchmarking (RandomForest, XGBoost, LightGBM)
- [ ] Stratified k-fold cross-validation for all supervised models
- [ ] Full sklearn Pipeline encapsulation
- [ ] LangGraph agentic workflow integration
- [ ] RAG pipeline using Chroma or FAISS for learning resource retrieval
- [ ] Session-based memory for multi-turn student coaching
- [ ] Chain-of-thought personalized weekly study plan generation
- [ ] Conversational interface integrated into the AcadIQ frontend
- [ ] Silhouette score and Davies-Bouldin evaluation for clustering

---

## Team

| Name | Role |
|---|---|
| Rajdeep Sanyal | ML Lead and Project Coordinator |
| Rajat Srivastava | Data Engineering and EDA |
| Anand Mishra | Clustering and Visualization |
| Omved Nagre | Application Development and Deployment |

---

## License

This project was developed as part of the GenAI Capstone academic program. All rights reserved by the authors. For any inquiries regarding reuse or collaboration, contact the team via the repository issue tracker.
