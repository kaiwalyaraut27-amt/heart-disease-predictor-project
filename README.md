# 🫀 CardioScan AI — Heart Disease Prediction

A machine learning web application that predicts the probability of heart disease from clinical patient data. Built with **Scikit-learn**, **Streamlit**, and a tuned **Logistic Regression** model achieving **ROC-AUC > 0.85**.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?style=flat-square&logo=streamlit)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-orange?style=flat-square&logo=scikit-learn)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 📋 Table of Contents

- [Problem Statement](#-problem-statement)
- [Dataset](#-dataset)
- [Project Structure](#-project-structure)
- [Feature Engineering](#-feature-engineering)
- [Models Evaluated](#-models-evaluated)
- [Results](#-results)
- [Installation](#-installation)
- [Usage](#-usage)
- [Screenshots](#-screenshots)
- [Key Findings](#-key-findings)
- [Limitations](#-limitations)
- [Disclaimer](#-disclaimer)

---

## 🎯 Problem Statement

Early detection of heart disease allows doctors to intervene before severe complications occur. This project builds a reliable binary classification model that estimates disease probability from patient clinical measurements.

**Target variable:**
- `1` → Heart disease present
- `0` → No heart disease

**Priority:** Minimizing false negatives — missing a real disease case is more dangerous than a false positive.

---

## 📊 Dataset

The Heart Disease dataset contains several hundred patient records with clinical and diagnostic measurements including:

| Feature | Description |
|---|---|
| `age` | Patient age in years |
| `sex` | Sex (0 = Female, 1 = Male) |
| `cp` | Chest pain type (0–3) |
| `trestbps` | Resting blood pressure (mmHg) |
| `chol` | Serum cholesterol (mg/dl) |
| `fbs` | Fasting blood sugar > 120 mg/dl |
| `restecg` | Resting ECG results (0–2) |
| `thalach` | Maximum heart rate achieved |
| `exang` | Exercise-induced angina |
| `oldpeak` | ST depression induced by exercise |
| `slope` | Slope of peak exercise ST segment |
| `ca` | Number of major vessels (0–3) |
| `thal` | Thalassemia type (1–3) |

---

## 📁 Project Structure

```
cardioscan-ai/
│
├── app.py                      # Streamlit web application
│
├── heart_model.pkl             # Trained Logistic Regression model
├── heart_features.json         # Ordered feature list for inference
├── heart_model_metadata.json   # Model metadata and parameters
├── heart_final.csv             # Final engineered dataset
├── predictions_log.json        # Saved prediction logs
│
├── charts/
│   ├── chart_confusion_final.png
│   ├── chart_roc_final.png
│   ├── chart_pr_curve.png
│   ├── chart_model_comparison.png
│   └── eda_overview.png
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Feature Engineering

Seven engineered features were added to improve predictive power, derived from standard clinical thresholds:

| Engineered Feature | Logic | Clinical Meaning |
|---|---|---|
| `high_chol` | cholesterol > 240 | High cholesterol flag |
| `high_bp` | resting BP > 140 | Hypertension flag |
| `hr_ratio` | thalach / (220 − age) | Heart rate as % of expected max |
| `sig_oldpeak` | oldpeak > 2.0 | Significant ST depression |
| `age_group_middle` | 40 ≤ age < 55 | Middle-aged group |
| `age_group_senior` | 55 ≤ age < 70 | Senior group |
| `age_group_elderly` | age ≥ 70 | Elderly group |

---

## 🤖 Models Evaluated

Five models were compared using cross-validation with ROC-AUC scoring:

| Model | Notes |
|---|---|
| **Logistic Regression** ✅ | Best balance of performance + generalization |
| Random Forest | Strong but showed greater overfitting |
| Gradient Boosting | High accuracy, larger train-test gap |
| Decision Tree | Interpretable but lower generalization |
| K-Nearest Neighbors | Sensitive to feature scaling |

**Winner: Logistic Regression** — tuned via `RandomizedSearchCV` optimizing ROC-AUC. Final hyperparameters covered regularization strength (C), solver, and balanced class weighting.

---

## 📈 Results

| Metric | Score |
|---|---|
| ROC-AUC | > 0.85 |
| Sensitivity (Recall) | High — prioritized to minimize missed cases |
| Specificity | Balanced |
| F1 Score | Strong cross-validation stability |

The model achieves good separation between positive and negative cases with low variance across folds.

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/your-username/cardioscan-ai.git
cd cardioscan-ai

# Install dependencies
pip install -r requirements.txt
```

**requirements.txt:**
```
streamlit
scikit-learn
pandas
numpy
joblib
```

---

## 💻 Usage

```bash
streamlit run app.py
```

Make sure the following files are in the same directory as `app.py`:
- `heart_model.pkl`
- `heart_features.json`

The app will open at `http://localhost:8501`.

### Risk Output Categories

| Probability | Category | Action |
|---|---|---|
| 0.00 – 0.30 | ✅ Low Risk | Routine monitoring |
| 0.30 – 0.50 | 🔵 Mild Risk | Lifestyle improvements |
| 0.50 – 0.70 | ⚠️ Moderate Risk | Medical evaluation advised |
| 0.70 – 0.85 | 🚨 High Risk | Clinical consultation recommended |
| 0.85 – 1.00 | 🛑 Critical Risk | Immediate medical assessment |

---

## 🔍 Key Findings

From EDA and correlation analysis, the strongest predictors of heart disease were:

- **Chest pain type (`cp`)** — higher severity strongly associated with disease
- **Maximum heart rate (`thalach`)** — lower values during exercise correlated with higher risk
- **ST depression (`oldpeak`)** — abnormal values were a strong positive indicator
- **Number of major vessels (`ca`)** — higher count associated with disease

---

## ⚠️ Limitations

- The dataset is relatively small, which limits generalization to diverse populations
- The model has **not been clinically validated** and is not intended for real medical use
- Performance may vary across different hospitals, demographics, or data collection methods

---

## 🩺 Disclaimer

> This tool is for **educational purposes only** and does not replace professional medical diagnosis. All predictions should be reviewed by a qualified healthcare professional. Do not make medical decisions based solely on this model's output.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
