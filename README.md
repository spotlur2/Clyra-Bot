# Clyra-Bot NLP System

---

# Project Overview

This project is a Discord AutoModeration system powered by NLP techniques.  
It analyzes user messages in real time and determines whether they should be:

- 🟢 Allowed
- 🟡 Warned
- 🔴 Deleted
- 🟣 Mute
- ⚫ Ban

The moderation system combines multiple NLP signals including toxicity detection, sentiment analysis, sarcasm detection, and spam behavior analysis into a unified feature fusion model. A decision system then calculates a risk score and selects the final moderation action.

The project also includes an interactive Streamlit dashboard for visualizing moderation decisions, feature scores, explanations, and moderation history.

---

# Key Features

## 1) Multi-model NLP pipeline

The system integrates several NLP components:

- Toxicity detection
- Sentiment analysis
- Emotion detection
- Sarcasm detection
- Spam classification
- Behavioral spam analysis
- Feature fusion
- Rule + score-based moderation decision system
- Interactive moderation dashboard
- Context-aware message analysis

---

## 2) Interactive Dashboard

The Streamlit dashboard provides:

- Real-time message moderation
- Risk score visualization
- Feature importance explanations
- Moderation history tracking
- Raw model output inspection

---

## 3) Context-Aware Analysis

The system supports contextual moderation by analyzing previous chat messages alongside the current message.

Example:

```text
Context:
    "we are joking lol"

Message:
    "shut up idiot"
```

This helps the system distinguish between harmful toxicity and casual banter.

---

# System Architecture

```text
Input Message
    ↓
Toxicity Detection
Sentiment + Emotion + Sarcasm
Spam + Behavioral Analysis
    ↓
Feature Fusion
    ↓
Risk Score Calculation
    ↓
Decision System
    ↓
Dashboard Output
```

---

# Project Structure

```text
Clyra-Bot/
│
├── dashboard.py              # Streamlit moderation dashboard
├── main.py                   # Main NLP pipeline
├── fusion.py                 # Feature fusion module
├── decision_system.py        # Moderation decision logic
├── toxicity.py               # Toxicity detection
├── sentiment.py              # Sentiment/emotion/sarcasm analysis
├── spam_behavioral.py        # Spam + behavioral analysis
├── evaluation.py             # Evaluation script
├── evaluation_data.json      # Evaluation dataset
├── requirements.txt
└── README.md
```

---

# Requirements

## Software

- Python 3.9+
- pip

## Main Libraries

- transformers
- torch
- streamlit
- pandas
- numpy
- scikit-learn

---

# Installation

## Step 1: Clone the Repository

```bash
git clone https://github.com/spotlur2/Clyra-Bot.git
cd Clyra-Bot
```

---

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Project

## Run the Interactive Dashboard

```bash
streamlit run dashboard.py
```

or

```bash
python -m streamlit run dashboard.py
```

Then open the local Streamlit address shown in the terminal (usually http://localhost:8501).

The dashboard allows users to:

- Enter Discord messages
- Add context messages
- View moderation decisions
- Analyze feature scores
- Inspect risk explanations

---

## Optional: Run the Backend Pipeline Only

```bash
python main.py
```

This runs console-based examples of the moderation pipeline without the dashboard UI.

---

# Example Test Cases

## 1) Normal Message

```text
"Hey everyone, how are you doing today?"
```

→ 🟢 Allow

---

## 2) Toxic Message

```text
"You are so stupid and useless"
```

→ 🔴 Delete

---

## 3) Severe Threat

```text
"I will hurt you"
```

→ ⚫ Ban

---

## 4) Spam Message

```text
"FREE MONEY CLICK HERE http://spam.com NOW!!!"
```

→ 🔴 Delete

---

# Decision Logic

The system computes a weighted risk score using fused NLP features.

Simplified example:

```text
risk =
    toxicity +
    threat +
    spam +
    anger +
    behavioral signals
```

The system also includes hard moderation rules for severe threats, hate speech, and aggressive spam behavior.

Example moderation thresholds:

```text
0.00 – 0.27         → Allow
0.28 – 0.49         → Warn
0.50 – 0.74         → Delete
0.75+               → Mute
Extreme threat/hate → Ban
```

Based on the implementation in `decision_system.py`

---

# Evaluation

The project includes an evaluation pipeline using labeled moderation examples stored in `evaluation_data.json`.

## To run evaluation

```bash
python evaluation.py
```
## Evaluation Results

The moderation system was evaluated using a labeled dataset containing:
- normal conversation messages
- toxic insults
- severe threats
- spam messages
- contextual banter examples

The baseline system uses rule-based keyword filtering and spam pattern matching without contextual understanding, sentiment analysis, or feature fusion.

## Overall Results

|             System           |  Accuracy | 
|------------------------------|-----------|
| Baseline Rule-Based System   |   76.67%  |   
| Clyra-Bot                    |   66.67%  | 

## Clyra-Bot Per-Class Performance

| Action  | Precision | Recall | F1-score |
|---------|-----------|--------|----------|
| Allow   |   0.4615  | 1.0000 |  0.6316  |  
| Warn    |   0.6667  | 0.5714 |  0.6154  |
| Delete  |   0.8750  | 0.8750 |  0.8750  |
| Mute    |   1.0000  | 0.2500 |  0.4000  |
| Ban     |   1.0000  | 0.4000 |  0.5714  |

## Additional Metrics
```text
Accuracy: 66.67%

Macro Average F1-score: 0.6187
Weighted Average F1-score: 0.6518
```

## Observations

The baseline system achieved higher overall accuracy because it relied on direct keyword matching and fixed moderation rules. However, the baseline system could not handle nuanced moderation actions such as contextual warnings and often produced strict moderation decisions.

Clyra-bot performed better on many contextual moderation examples involving joking or conversational banter. For example, messages such as:

    "you're trash lol"
    "idiot haha"

were handled more appropriately by the contextual moderation system compared to the baseline system.

The system performed best on:
  - toxic message detection
  - delete-level moderation
  - contextual warning detection
  - explicit toxic language

Some severe threat and spam examples remain challenging due to:
  - sarcasm ambiguity
  - contextual interpretation
  - indirect threats
  - spam threshold tuning
  - conversational banter

## Future improvements may include:
- larger labeled datasets
- fine-tuned moderation models
- stronger contextual memory
- improved spam or phishing detection
- user behavior tracking across longer conversations

---

# NLP Models Used

## Toxicity Detection

`unitary/toxic-bert`

## Sentiment Analysis

`cardiffnlp/twitter-roberta-base-sentiment-latest`

## Emotion Detection

`j-hartmann/emotion-english-distilroberta-base`

## Sarcasm Detection

`cardiffnlp/twitter-roberta-base-irony`

## Spam Classification

`mshenoda/roberta-spam`
