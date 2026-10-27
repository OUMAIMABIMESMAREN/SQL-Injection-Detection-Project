"""
app.py — Interface web Streamlit pour la détection d'injections SQL
Projet académique : Master BDSI — Module Cyber Sécurité
Étudiante : Oumaima Bimesmaren — 2025-2026
"""

import re
import os
import joblib
import streamlit as st

# ─── Configuration de la page ────────────────────────────────────────────────
st.set_page_config(
    page_title="SQL Injection Detector",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── CSS personnalisé ─────────────────────────────────────────────────────────
st.markdown("""
<style>
  .stApp { background-color: #0f1117; }

  .main-title {
      background: linear-gradient(135deg, #1a1f2e, #252a3a);
      border-left: 5px solid #3498db;
      border-radius: 10px;
      padding: 20px 28px;
      margin-bottom: 24px;
  }
  .main-title h1 { color: #ecf0f1; margin: 0; font-size: 1.6rem; }
  .main-title p  { color: #95a5a6; margin: 6px 0 0; font-size: 0.9rem; }

  .result-safe {
      background: linear-gradient(135deg, #0d2818, #1a4a2e);
      border: 2px solid #27ae60;
      border-radius: 12px;
      padding: 20px 24px;
      text-align: center;
      margin-top: 16px;
  }
  .result-danger {
      background: linear-gradient(135deg, #2c0a0a, #4a1515);
      border: 2px solid #e74c3c;
      border-radius: 12px;
      padding: 20px 24px;
      text-align: center;
      margin-top: 16px;
  }
  .result-safe h2   { color: #2ecc71; font-size: 1.5rem; margin: 0; }
  .result-danger h2 { color: #e74c3c; font-size: 1.5rem; margin: 0; }
  .result-safe p, .result-danger p { color: #bdc3c7; margin: 8px 0 0; }

  .stTextArea textarea {
      background-color: #1a1f2e !important;
      color: #ecf0f1 !important;
      border: 1px solid #3498db !important;
      border-radius: 8px !important;
      font-family: 'Courier New', monospace !important;
      font-size: 0.95rem !important;
  }

  .stButton > button {
      background: linear-gradient(135deg, #2980b9, #3498db);
      color: white;
      border: none;
      border-radius: 8px;
      padding: 0.6rem 2rem;
      font-size: 1.05rem;
      font-weight: 600;
      width: 100%;
  }
  .stButton > button:hover {
      background: linear-gradient(135deg, #1a6a99, #2980b9);
  }

  .footer {
      text-align: center;
      color: #4a5568;
      font-size: 0.8rem;
      margin-top: 40px;
      padding-top: 16px;
      border-top: 1px solid #2c3e50;
  }
</style>
""", unsafe_allow_html=True)


# ─── Initialisation du session_state ─────────────────────────────────────────
# Cela permet de mémoriser la saisie et le résultat entre les reruns Streamlit
if "query_value" not in st.session_state:
    st.session_state.query_value = ""
if "result" not in st.session_state:
    st.session_state.result = None   # None = pas encore analysé
if "confiance" not in st.session_state:
    st.session_state.confiance = None


# ─── Chargement du modèle ────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH  = os.path.join(BASE_DIR, "models", "sql_injection_detector.pkl")
VEC_PATH    = os.path.join(BASE_DIR, "models", "tfidf_vectorizer.pkl")

@st.cache_resource(show_spinner=False)
def charger_modele():
    model = joblib.load(MODEL_PATH)
    vec   = joblib.load(VEC_PATH)
    return model, vec

try:
    model, vectorizer = charger_modele()
    modele_ok = True
except FileNotFoundError:
    modele_ok = False


# ─── Fonction de prédiction ───────────────────────────────────────────────────
def detect_sql_injection(query: str):
    q = re.sub(r'\s+', ' ', query.lower().strip())
    X = vectorizer.transform([q])
    pred = int(model.predict(X)[0])
    proba = None
    if hasattr(model, "predict_proba"):
        proba = float(model.predict_proba(X)[0][pred])
    return pred, proba


# ─── Interface ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-title">
  <h1>🔒 Détecteur d'Injections SQL</h1>
  <p>Master BDSI · Module Cyber Sécurité · Oumaima Bimesmaren · 2025-2026</p>
</div>
""", unsafe_allow_html=True)

if not modele_ok:
    st.error("⚠️ Modèle introuvable. Exécutez d'abord le notebook Jupyter pour générer les fichiers .pkl.")
    st.stop()

# ─── Zone de saisie ───────────────────────────────────────────────────────────
st.markdown("### 📝 Saisir une requête SQL à analyser")

query_input = st.text_area(
    label="Requête SQL",
    label_visibility="collapsed",
    value=st.session_state.query_value,
    placeholder="Exemple : SELECT * FROM users WHERE id = 1",
    height=120,
    key="sql_textarea"
)

# Mémoriser ce que l'utilisateur a tapé
st.session_state.query_value = query_input

# ─── Bouton Analyser ──────────────────────────────────────────────────────────
col_btn, _ = st.columns([1, 2])
with col_btn:
    analyser = st.button("🔍 Analyser", use_container_width=True)

if analyser:
    if not query_input.strip():
        st.warning("⚠️ Veuillez saisir une requête SQL avant d'analyser.")
        st.session_state.result = None
    else:
        with st.spinner("Analyse en cours ..."):
            pred, conf = detect_sql_injection(query_input)
        st.session_state.result   = pred
        st.session_state.confiance = conf

# ─── Affichage du résultat ────────────────────────────────────────────────────
if st.session_state.result is not None:
    st.markdown("---")
    st.markdown("### 📊 Résultat de l'analyse")

    pred = st.session_state.result
    conf = st.session_state.confiance
    conf_str = f"<p style='margin-top:10px; font-size:1rem;'><b>Confiance : {conf*100:.1f} %</b></p>" if conf else ""

    if pred == 1:
        st.markdown(f"""
        <div class="result-danger">
            <h2>🚨 SQL Injection détectée</h2>
            <p>Cette requête contient des motifs caractéristiques d'une tentative d'injection SQL.</p>
            <p style="color:#e74c3c;">{conf_str}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-safe">
            <h2>✅ Requête normale</h2>
            <p>Cette requête SQL semble légitime. Aucun motif d'injection détecté.</p>
            <p style="color:#2ecc71;">{conf_str}</p>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("🔎 Détails techniques"):
        st.code(f"""Requête analysée : {st.session_state.query_value}
Classe prédite  : {'1 — SQL Injection' if pred == 1 else '0 — Requête légitime'}
Confiance       : {f'{conf*100:.2f} %' if conf else 'N/A'}""")

# ─── Exemples rapides ─────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🧪 Exemples à tester")

exemples = {
    "SELECT légitime" : "SELECT * FROM products WHERE id = 10",
    "OR '1'='1'"      : "' OR '1'='1",
    "UNION SELECT"    : "' UNION SELECT username, password FROM users --",
    "DROP TABLE"      : "'; DROP TABLE users; --",
    "INSERT légitime" : "INSERT INTO orders (product_id, qty) VALUES (3, 1)",
}

cols = st.columns(len(exemples))
for col, (label, exemple) in zip(cols, exemples.items()):
    with col:
        if st.button(label, key=f"ex_{label}"):
            st.session_state.query_value = exemple
            st.session_state.result = None
            st.rerun()

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  Projet académique · Master BDSI · Oumaima Bimesmaren · 2025-2026<br>
  Détection par Machine Learning (TF-IDF + Random Forest / Logistic Regression)
</div>
""", unsafe_allow_html=True)
