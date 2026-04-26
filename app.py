import streamlit as st
import pandas as pd
from collections import defaultdict

st.set_page_config(page_title="Medi Raksha", layout="centered")

# 🎨 Styling
st.markdown("""
<style>

/* Hide default Streamlit header */
header {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Background */
.stApp {
    background-color: #fcffb7;
}

/* Title */
.logo-title {
    text-align: center;
    font-size: 45px;
    font-weight: 700;
    color: #155724;
    margin-top: -20px;
    margin-bottom: 15px;
}

/* Section title */
.section-title {
    color: #007bff;
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 8px;
}

/* Result title */
.result-title {
    color: black;
    font-size: 22px;
    font-weight: 600;
    margin-top: 10px;
    margin-bottom: 8px;
}

/* Compact disease card */
.disease-card {
    background-color: #d4edda;
    color: #0b3d0b;
    padding: 8px 12px;
    border-radius: 8px;
    margin-bottom: 6px;
    font-size: 16px;
    font-weight: 600;
}

/* Matched symptoms text */
.symptom-text {
    font-size: 13px;
    color: #333;
    margin-bottom: 6px;
}

/* Button */
div[data-testid="stButton"] > button {
    background-color:#28a745 !important;
    color:white !important;
    border:none !important;
    transition: all 0.2s ease !important;
}

div[data-testid="stButton"] > button:hover {
    background-color:#218838 !important;
}

div[data-testid="stButton"] > button:active {
    transform: scale(1.15) !important;
    background-color:#007bff !important;
}

</style>
""", unsafe_allow_html=True)

# 🏷️ Header
st.markdown(
    '<div class="logo-title">🩺 Medi Raksha Disease Prediction</div>',
    unsafe_allow_html=True
)

# 📂 Load dataset
df = pd.read_csv("dataset.csv").fillna("")
sym_cols = [c for c in df.columns if "Symptom" in c]

# 🧠 Extract symptoms
all_symptoms = sorted({
    str(s).strip().lower()
    for col in sym_cols
    for s in df[col]
    if str(s).strip()
})

# 🏥 Disease mapping
dis_sym = defaultdict(set)
for _, r in df.iterrows():
    for c in sym_cols:
        val = str(r[c]).strip().lower()
        if val:
            dis_sym[r['Disease']].add(val)

# 🔍 Section title
st.markdown(
    '<div class="section-title">Type or Select Symptoms</div>',
    unsafe_allow_html=True
)

# 🔍 Multiselect
selected = st.multiselect(
    "",
    options=all_symptoms,
    format_func=lambda x: x.replace("_", " ").title()
)

# 🧪 Prediction
if st.button("🏥 Show Diseases", use_container_width=True):
    if not selected:
        st.warning("Please select at least one symptom.")
    else:
        sel_set = set(selected)

        scores = [
            (d, len(sel_set & s) / len(sel_set | s), list(sel_set & s))
            for d, s in dis_sym.items()
            if sel_set & s
        ]

        if not scores:
            st.error("No matching disease found.")
        else:
            top_results = sorted(scores, key=lambda x: x[1], reverse=True)[:3]

            st.markdown(
                '<div class="result-title">Most Possible Diseases:</div>',
                unsafe_allow_html=True
            )

            # ✅ Compact display (NO SCROLL NEEDED)
            for d, sc, m in top_results:
                st.markdown(
                    f'<div class="disease-card">{d} ({sc:.0%} match)</div>',
                    unsafe_allow_html=True
                )
                st.markdown(
                    f'<div class="symptom-text">Matched: {", ".join([x.replace("_"," ").title() for x in m])}</div>',
                    unsafe_allow_html=True
                )