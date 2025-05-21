
import os
import pandas as pd
import streamlit as st

@st.cache_data
def carica_dati_generali(path):
    if not os.path.exists(path):
        st.error("File non trovato.")
        return None
    try:
        df = pd.read_excel(path, sheet_name="Dati sprint")
        df.columns = ["Campo", "Valore"]
        df["Valore"] = df["Valore"].astype(str).str.replace(",", ".").str.replace("%", "")
        df["Valore"] = pd.to_numeric(df["Valore"], errors="coerce")
        return {
            "lunghezza": df[df["Campo"].str.contains("lunghezza", case=False)]["Valore"].values[0],
            "dislivello": df[df["Campo"].str.contains("dislivello", case=False)]["Valore"].values[0],
            "pendenza": df[df["Campo"].str.contains("pendenza", case=False)]["Valore"].values[0],
        }
    except Exception as e:
        st.error(f"Errore nel caricamento dati generali: {e}")
        return None

def carica_atleti(path):
    try:
        df = pd.read_excel(path, usecols=[0])
        return df.iloc[:, 0].dropna().astype(str).unique().tolist()
    except:
        df = pd.read_excel(path, header=None, usecols=[0])
        return df.iloc[:, 0].dropna().astype(str).unique().tolist()

def carica_dati_atleta(nome, tecnica):
    path = f"data/{nome}.xlsx"
    tecnica = tecnica.lower().strip().capitalize()
    if not os.path.exists(path):
        return None, None
    xls = pd.ExcelFile(path)
    if tecnica not in xls.sheet_names:
        return None, None
    df = pd.read_excel(xls, sheet_name=tecnica, header=None)
    meta = {
        "data": df[df[0].str.lower() == "data"][1].values[0],
        "ora": df[df[0].str.lower() == "ora"][1].values[0],
        "strumenti": df[df[0].str.lower() == "strumenti"][1].values[0],
        "stile": df[df[0].str.lower() == "stile"][1].values[0],
    }
    return df, meta

def carica_lattato(path, tecnica):
    try:
        df = pd.read_excel(f"data/{path}.xlsx", sheet_name=tecnica, header=None)
        idx = df[df.iloc[:, 0].astype(str).str.contains("lattato", case=False)].index
        if not idx.empty:
            r = idx[0]
            return df.iloc[r - 1, 1:].tolist(), df.iloc[r, 1:].tolist()
        return [], []
    except:
        return [], []

def carica_split_segmenti(path, tecnica):
    try:
        df = pd.read_excel(f"data/{path}.xlsx", sheet_name=tecnica, skiprows=20, usecols="A:F")
        return df.dropna(how="all")
    except:
        return pd.DataFrame()
