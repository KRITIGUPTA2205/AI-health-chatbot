import streamlit as st
import pandas as pd
import pickle
import difflib

# ---------------- PAGE SETUP ----------------
st.set_page_config(
    page_title="🩺 AI Health Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- LOAD MODEL ----------------
with open("model.pkl", "rb") as f:
    best_model = pickle.load(f)

with open("symptoms.pkl", "rb") as f:
    symptoms_list = pickle.load(f)

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_symptoms" not in st.session_state:
    st.session_state.conversation_symptoms = set()

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
/* General page padding */
.block-container {
    padding-top: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* User bubble */
[data-testid="stChatMessage"][data-testid*="user"] {
    background: linear-gradient(145deg, #d0f0c0, #b8e6a0);
    border-radius: 20px;
    padding: 12px 15px;
    margin-bottom: 12px;
    max-width: 80%;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

/* Bot bubble */
[data-testid="stChatMessage"][data-testid*="assistant"] {
    background: linear-gradient(145deg, #f0f0f0, #e0e0e0);
    border-radius: 20px;
    padding: 12px 15px;
    margin-bottom: 12px;
    max-width: 80%;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

/* Input box styling */
textarea {
    border-radius: 12px !important;
    border: 1px solid #ccc !important;
    padding: 10px !important;
}

/* Sidebar cards */
.stSidebar h3 {
    font-weight: bold;
}
.stSidebar .stMarkdown {
    background-color: #f7f7f7;
    border-radius: 12px;
    padding: 10px;
    margin-bottom: 10px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

/* Headings */
h1, h2, h3 {
    font-family: 'Arial', sans-serif;
}
</style>
""", unsafe_allow_html=True)

# ---------------- NLP FUNCTIONS ----------------
def normalize_input(user_input):
    user_input = user_input.lower()
    replacements = {
        "temperature": "high_fever",
        "fever": "high_fever",
        "fevr": "high_fever",
        "feels it is high": "high_fever",
        "tired": "fatigue",
        "throwing up": "vomiting",
        "vomit sensation": "vomiting",
        "nauseous": "vomiting",
        "head pain": "headache",
        "stomach ache": "stomach_pain",
        "abdominal pain": "stomach_pain",
        "fainting": "dizziness",
        "faintinf": "dizziness",
        "feeling faint": "dizziness",
        "dizzy": "dizziness",
        "backache": "back_pain",
        "skin peeling": "skin_peeling"
    }
    for k, v in replacements.items():
        user_input = user_input.replace(k, v)
    return user_input

def find_closest_symptom(word, symptoms_list):
    match = difflib.get_close_matches(word, symptoms_list, n=1, cutoff=0.7)
    return match[0] if match else None

def input_to_vector(user_input, symptoms_list):
    user_input = normalize_input(user_input)
    input_vector = [0] * len(symptoms_list)
    words = set(user_input.replace(",", " ").split())
    stop_words = {"and", "in", "on", "at", "with", "have", "i", "also", "is", "it"}
    words = {w for w in words if w not in stop_words}
    for w in words:
        symptom = find_closest_symptom(w, symptoms_list)
        if symptom:
            idx = symptoms_list.index(symptom)
            input_vector[idx] = 1
    return input_vector

# ---------------- ADVICE FUNCTION ----------------
def get_advice(disease):
    precautions = {
        "Diabetes": ["Monitor sugar", "Healthy diet", "Exercise"],
        "Dengue": ["Stay hydrated", "Avoid mosquitoes", "Consult doctor"],
        "Malaria": ["Use mosquito nets", "Take medication"],
        "Common Cold": ["Rest", "Drink fluids"],
        "Pneumonia": ["Consult doctor", "Take medication"],
        "Heart Attack": ["Seek emergency help immediately"],
        "Typhoid": ["Drink clean water", "Take antibiotics"],
        "Tuberculosis": ["Complete medication course"]
    }
    if disease in precautions:
        return precautions[disease]
    disease_lower = disease.lower()
    if "hepatitis" in disease_lower:
        return ["Avoid alcohol", "Healthy diet", "Consult doctor"]
    elif "infection" in disease_lower:
        return ["Maintain hygiene", "Consult doctor"]
    elif "allergy" in disease_lower:
        return ["Avoid allergens", "Take antihistamines"]
    elif "pain" in disease_lower or "arthritis" in disease_lower:
        return ["Rest", "Apply hot/cold pack"]
    else:
        return ["Consult a healthcare professional"]

# ---------------- CHATBOT LOGIC ----------------
def chatbot_logic(user_input, best_model, symptoms_list, session_state):
    user_input_lower = user_input.lower()
    if "reset" in user_input_lower or "new" in user_input_lower:
        session_state["conversation_symptoms"] = set()
        return "🔄 New session started."
    if user_input_lower.startswith(("i have", "i am having", "suffering from")) and "also" not in user_input_lower:
        session_state["conversation_symptoms"] = set()
    vector = input_to_vector(user_input, symptoms_list)
    if sum(vector) == 0:
        return "❌ I couldn't detect any valid symptoms. Please describe symptoms like fever, headache, vomiting."
    detected = {symptoms_list[i] for i, v in enumerate(vector) if v == 1}
    all_symptoms = session_state.get("conversation_symptoms", set())
    all_symptoms.update(detected)
    if len(all_symptoms) > 10:
        all_symptoms = set(list(all_symptoms)[-10:])
    session_state["conversation_symptoms"] = all_symptoms
    final_vector = [1 if s in session_state["conversation_symptoms"] else 0 for s in symptoms_list]
    input_df = pd.DataFrame([final_vector], columns=symptoms_list)
    if sum(final_vector) < 2:
        return "⚠️ Please provide more symptoms for accurate prediction."
    probs = best_model.predict_proba(input_df)[0]
    threshold = 0.25
    serious_diseases = ["Heart Attack", "Aids", "Paralysis", "Pneumonia"]
    top_indices = [i for i, p in enumerate(probs) if p >= 0.05]
    top_indices_sorted = sorted(
        top_indices,
        key=lambda i: (best_model.classes_[i] in serious_diseases, -probs[i])
    )
    response = "🧠 Symptoms: " + ", ".join([s.replace("_", " ") for s in session_state["conversation_symptoms"]]) + "\n\n"
    response += "🩺 Possible Diseases:\n\n"
    for idx in top_indices_sorted[:3]:
        disease = best_model.classes_[idx]
        prob = probs[idx]
        if prob < threshold:
            response += f"• {disease} ({prob:.2f}) ⚠️ Low confidence\n"
        else:
            response += f"• {disease} ({prob:.2f})\n"
        advice = get_advice(disease)
        for a in advice:
            response += f"  - {a}\n"
        response += "\n"
    response += "👉 Do you have any other symptoms?\n⚠️ Not a medical diagnosis."
    return response

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙️ Options")
    if st.button("🔄 Reset Chat"):
        st.session_state.messages = []
        st.session_state.conversation_symptoms = set()
        st.success("Chat reset!")
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.write("• Type symptoms naturally")
    st.write("• Add more symptoms for accuracy")
    st.write("• Use 'reset' to start fresh")

# ---------------- HEADER ----------------
st.markdown("""
<h1 style='text-align: center; font-weight: bold;'>🩺 AI Health Assistant</h1>
<p style='text-align: center; color: gray;'>Chat naturally — describe your symptoms</p>
""", unsafe_allow_html=True)

st.caption("Describe your symptoms like chatting with a doctor")

# ---------------- CHAT DISPLAY ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- INPUT BOX ----------------
user_input = st.chat_input("Type your symptoms...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    response = chatbot_logic(user_input, best_model, symptoms_list, st.session_state)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

# ---------------- FOOTER ----------------
st.markdown("""
<hr>
<p style='text-align: center; color: gray;'>⚠️ This is not a medical diagnosis. Consult a doctor.</p>
""", unsafe_allow_html=True)