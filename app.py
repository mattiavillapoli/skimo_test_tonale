
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import utils__data_loader as dl

st.set_page_config(page_title="Test Skimo – Tonale 2025", layout="wide")

# --- STILE ---
st.markdown("""
    <style>
        .main { background-color: #ffffff; color: #222222; }
        h1, h2, h3 { font-weight: 800; }
        .metric-box {
            background: #f0f0f0;
            padding: 10px;
            border-radius: 8px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    st.image("data__logo fisi.png", width=100)
with col2:
    st.image("data__logo polimi.jpg", width=100)
with col3:
    st.markdown("<h1>Test Skimo<br>Tonale 2025</h1>", unsafe_allow_html=True)

# --- DATI GENERALI ---
st.markdown("### 📊 Dati Generali Sprint")
dati = dl.carica_dati_generali("data__sum up.xlsx")
if dati:
    col1, col2, col3 = st.columns(3)
    col1.metric("📏 Lunghezza", f"{dati['lunghezza']} m")
    col2.metric("⛰️ Dislivello", f"{dati['dislivello']} m")
    col3.metric("📉 Pendenza", f"{dati['pendenza']} %")
else:
    st.error("Dati generali non disponibili.")

# --- SELEZIONE ATLETA ---
st.markdown("---")
st.subheader("🎽 Seleziona un atleta")
atleti = dl.carica_atleti("data__atleti.xlsx")
atleta = st.selectbox("Scegli atleta", atleti)

# --- SELEZIONE TECNICA ---
tecnica = st.selectbox("Seleziona tecnica", ["Tecnica libera", "Tecnica alternata", "Tecnica doppia"])

# --- DATI ATLETA ---
df, meta = dl.carica_dati_atleta(atleta, tecnica)
if df is not None:
    st.markdown("---")
    st.subheader(f"📄 Dati prova – {tecnica} – {atleta}")
    st.write(f"📅 **Data:** {meta['data']}")
    st.write(f"🕒 **Ora:** {meta['ora']}")
    st.write(f"🛠️ **Strumenti:** {meta['strumenti']}")
    st.write(f"⛷️ **Stile:** {meta['stile']}")

    st.markdown("### 📊 Performance")
    metriche = [
        "Durata", "Velocità media (Km/h)", "Velocità max (Km/h)",
        "VAM media (m/h)", "HR max", "HR media", "HR media recupero"
    ]
    col1, col2, col3 = st.columns(3)
    for i, met in enumerate(metriche):
        valore = None
        for _, row in df.iterrows():
            if str(row[0]).strip().lower() == met.lower():
                valore = row[1]
                break
        col = [col1, col2, col3][i % 3]
        if valore:
            col.markdown(f"<div class='metric-box'><b>{met}</b><br>{valore}</div>", unsafe_allow_html=True)
else:
    st.warning("⚠️ Nessun dato disponibile per l'atleta o la tecnica selezionata.")
