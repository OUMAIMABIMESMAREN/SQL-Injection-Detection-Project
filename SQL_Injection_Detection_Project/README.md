# 🔒 Détection des Requêtes SQL Malveillantes par Machine Learning

> Projet académique · Master BDSI (Big Data et Systèmes Intelligents)
> Module : Cyber Sécurité · Étudiante : **Oumaima Bimesmaren** · 2025-2026

---

## 📌 Description du projet

Ce projet développe un système intelligent de détection des injections SQL (*SQL Injection*) en utilisant des techniques de Machine Learning. Il classifie automatiquement chaque requête SQL en :

- **Classe 0** — Requête SQL **légitime**
- **Classe 1** — Requête SQL **malveillante** (SQL Injection)

Le pipeline complet couvre : génération du dataset, prétraitement NLP, vectorisation TF-IDF, entraînement de 4 modèles ML, évaluation comparative et déploiement via une interface Streamlit.

---

## 📁 Arborescence du projet

```
SQL_Injection_Detection_Project/
│
├── dataset/
│   └── sql_injection_dataset.csv     # 1200 requêtes (600 légitimes + 600 malveillantes)
│
├── models/
│   ├── sql_injection_detector.pkl    # Meilleur modèle entraîné (joblib)
│   └── tfidf_vectorizer.pkl          # Vectoriseur TF-IDF sauvegardé
│
├── notebooks/
│   └── SQL_Injection_Detection.ipynb # Notebook Jupyter complet (10 parties)
│
├── app.py                            # Interface web Streamlit
├── requirements.txt                  # Dépendances Python
└── README.md                         # Ce fichier
```

---

## ⚙️ Installation

### 1. Cloner le projet

```bash
git clone <url-du-repo>
cd SQL_Injection_Detection_Project
```

### 2. Créer un environnement virtuel (recommandé)

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## 🚀 Utilisation

### Exécuter le notebook Jupyter

```bash
cd notebooks
jupyter notebook SQL_Injection_Detection.ipynb
```

Exécuter toutes les cellules dans l'ordre (**Kernel → Restart & Run All**).  
Le notebook génère automatiquement le dataset et entraîne les modèles.

### Lancer l'interface Streamlit

*Après avoir exécuté le notebook au moins une fois (pour générer les .pkl) :*

```bash
streamlit run app.py
```

L'interface s'ouvre dans le navigateur à l'adresse `http://localhost:8501`.

### Utiliser la fonction de détection en Python

```python
import joblib, re

model      = joblib.load("models/sql_injection_detector.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")

def detect_sql_injection(query):
    q = re.sub(r'\s+', ' ', query.lower().strip())
    X = vectorizer.transform([q])
    return "SQL Injection détectée" if model.predict(X)[0] == 1 else "Requête normale"

print(detect_sql_injection("SELECT * FROM users WHERE username='admin' OR '1'='1'"))
# → SQL Injection détectée
print(detect_sql_injection("SELECT * FROM products WHERE id = 42"))
# → Requête normale
```

---

## 📊 Résultats

| Modèle | Accuracy | Precision | Recall | F1 Score |
|---|---|---|---|---|
| Logistic Regression | ~99.6 % | ~100 % | ~99.2 % | ~99.6 % |
| **Random Forest** | **~100 %** | **~100 %** | **~100 %** | **~100 %** |
| SVM | ~99.6 % | ~100 % | ~99.2 % | ~99.6 % |
| Naive Bayes | ~97.9 % | ~96.7 % | ~99.2 % | ~97.9 % |

> Le meilleur modèle est sélectionné automatiquement sur la base du **F1 Score**.

---

## 🛠️ Technologies utilisées

| Bibliothèque | Version | Rôle |
|---|---|---|
| Python | ≥ 3.10 | Langage principal |
| pandas | ≥ 2.0 | Manipulation du dataset |
| NumPy | ≥ 1.24 | Calcul numérique |
| scikit-learn | ≥ 1.3 | ML : TF-IDF, modèles, métriques |
| Matplotlib | ≥ 3.7 | Visualisations |
| Seaborn | ≥ 0.12 | Graphiques statistiques |
| Joblib | ≥ 1.3 | Persistance des modèles |
| Streamlit | ≥ 1.32 | Interface web |
| Jupyter | ≥ 7.0 | Notebook interactif |

---

## 📚 Références

- OWASP — SQL Injection : https://owasp.org/www-community/attacks/SQL_Injection
- Scikit-Learn Documentation : https://scikit-learn.org/stable/
- OWASP Top 10 : https://owasp.org/www-project-top-ten/

---

*Réalisé dans le cadre du module Cyber Sécurité — Master BDSI 2025-2026*
