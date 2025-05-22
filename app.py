# app.py - entry point per Streamlit
import streamlit as st
st.title('Test Skimo - Tonale 2025')

import streamlit as st
import utils__data_loader as dl

st.title("Skimo Tonale 2025")

# Caricamento dati generali
dati = dl.carica_dati_generali("data/sum up.xlsx")
if dati:
    st.metric("📏 Lunghezza", f"{dati['lunghezza']} m")
    st.metric("⛰️ Dislivello", f"{dati['dislivello']} m")
    st.metric("📉 Pendenza", f"{dati['pendenza']} %")

# Selezione atleta
lista_nomi = dl.carica_atleti("data/atleti.xlsx")
atleta = st.selectbox("Scegli atleta", lista_nomi)

# Selezione tecnica
tecnica = st.selectbox("Tecnica", ["Tecnica libera", "Tecnica alternata", "Tecnica doppia"])

# Dati specifici dell’atleta
df, meta = dl.carica_dati_atleta(atleta, tecnica)
if df is not None:
    st.subheader(f"Dati {atleta} – {tecnica}")
    st.write(meta)
