# 🏥 AI Health Chatbot

**An intelligent symptom-based disease prediction system powered by Machine Learning and Natural Language Processing.**

---

## 🎯 Overview

The AI Health Chatbot is a conversational application that helps users identify potential diseases based on their symptoms. It uses machine learning algorithms combined with fuzzy matching to provide accurate, confidence-scored predictions. The chatbot interface makes it easy and accessible for users to input their symptoms naturally.

---

## ✨ Key Features

- 🔍 **Smart Symptom Matching**: Fuzzy matching to handle varied symptom descriptions
- 🤖 **ML-Powered Predictions**: Random Forest Classifier for accurate disease prediction
- 📊 **Confidence Scores**: Top-3 disease predictions with confidence percentages
- 💬 **Conversational Interface**: User-friendly Streamlit chat interface
- 🎨 **Interactive UI**: Clean, responsive design for seamless interaction

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|----------|
| Backend | Python 3.x |
| Frontend/UI | Streamlit |
| ML Framework | Scikit-Learn (Random Forest) |
| Data Processing | Pandas, NumPy |
| Dataset | Kaggle Disease Prediction Dataset |

---

## 📂 Project Structure

```
AI-health-chatbot/
├── README.md
├── app.py                    # Main Streamlit application
├── models/
│   └── disease_classifier.pkl  # Trained Random Forest model
├── data/
│   ├── disease_symptoms.csv
│   └── raw_data/
└── notebooks/
    └── model_training.ipynb   # ML model development & analysis
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip or conda

### Installation

```bash
# Clone the repository
git clone https://github.com/KRITIGUPTA2205/AI-health-chatbot.git
cd AI-health-chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 💡 How It Works

1. **Input Processing**: User describes symptoms in natural language
2. **Symptom Matching**: System matches input to known symptoms using fuzzy logic
3. **Prediction**: Random Forest model predicts likely diseases
4. **Ranking**: Top 3 predictions displayed with confidence scores
5. **Output**: Results presented in easy-to-understand format

---

## 📊 Model Performance

- **Algorithm**: Random Forest Classifier
- **Training Data**: [Kaggle Disease Prediction Dataset](https://www.kaggle.com/)
- **Features**: Multi-symptom combinations

---

## 🎓 Learning Outcomes

This project demonstrates proficiency in:
- ✅ Machine Learning (Classification, Model Training)
- ✅ NLP & Text Processing (Fuzzy Matching)
- ✅ Data Preprocessing & Feature Engineering
- ✅ Web Application Development (Streamlit)
- ✅ Python Development Best Practices

---

## 🔮 Future Enhancements

- [ ] Add severity levels for symptoms
- [ ] Implement spell-checker for symptom input
- [ ] Integrate medical APIs for real-time data
- [ ] Add doctor recommendation system
- [ ] Deploy to cloud (HuggingFace Spaces, AWS, GCP)
- [ ] Support multiple languages

---

## 📝 Dataset Information

The project uses the Kaggle Disease Prediction Dataset containing:
- Multiple disease profiles
- Associated symptoms for each disease
- Structured data for training the classifier

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -m 'Add improvement'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the MIT License.

---

## 📧 Contact & Support

For questions or suggestions, please open an issue or reach out via GitHub.

---

**⭐ If you find this project helpful, please consider giving it a star!**