
import os
import pandas as pd
import streamlit as st

@st.cache_data
def carica_dati_generali(path):
    """Carica i dati generali dal foglio 'Dati sprint'."""
    if not os.path.exists(path):
        st.error(f"❌ File non trovato: {path}")
        return None
    try:
        df = pd.read_excel(path, sheet_name="Dati sprint")
        df.columns = ["Campo", "Valore"]
        df["Valore"] = df["Valore"].astype(str).str.replace(",", ".").str.replace("%", "")
        df["Valore"] = pd.to_numeric(df["Valore"], errors="coerce")
        return {
            "lunghezza": df[df["Campo"].str.contains("lunghezza", case=False, na=False)]["Valore"].values[0],
            "dislivello": df[df["Campo"].str.contains("dislivello", case=False, na=False)]["Valore"].values[0],
            "pendenza": df[df["Campo"].str.contains("pendenza", case=False, na=False)]["Valore"].values[0],
        }
    except Exception as e:
        st.error(f"Errore nel caricamento dati generali: {e}")
        return None

@st.cache_data
def carica_segmenti(path):
    """Carica i dati dei segmenti dal foglio 'Dati segmenti'."""
    try:
        df = pd.read_excel(path, sheet_name="Dati segmenti", index_col=0)
        df.columns = df.columns.str.strip()
        for col in df.columns:
            df[col] = df[col].astype(str).str.replace(",", ".").str.replace("%", "")
            df[col] = pd.to_numeric(df[col], errors="coerce")
        return df
    except Exception as e:
        st.error(f"Errore nel caricamento segmenti: {e}")
        return pd.DataFrame()

def carica_atleti(path):
    """Estrae i nomi degli atleti da un file Excel."""
    try:
        df = pd.read_excel(path, usecols=[0])
        return df.iloc[:, 0].dropna().astype(str).unique().tolist()
    except:
        df = pd.read_excel(path, header=None, usecols=[0])
        return df.iloc[:, 0].dropna().astype(str).unique().tolist()

def carica_dati_atleta(nome, tecnica):
    """Carica il file Excel dell'atleta per una tecnica specifica."""
    path = f"data/{nome}.xlsx"
    tecnica = tecnica.strip().lower().capitalize()
    if not os.path.exists(path):
        st.error(f"❌ File non trovato: {path}")
        return None, None
    try:
        xls = pd.ExcelFile(path)
        if tecnica not in xls.sheet_names:
            st.error(f"❌ Foglio '{tecnica}' non trovato in {nome}.xlsx")
            return None, None
        df = pd.read_excel(xls, sheet_name=tecnica, header=None)
        meta = {
            "data": _estrai_valore(df, "Data"),
            "ora": _estrai_valore(df, "Ora"),
            "strumenti": _estrai_valore(df, "Strumenti"),
            "stile": _estrai_valore(df, "Stile"),
        }
        return df, meta
    except Exception as e:
        st.error(f"Errore nel caricamento dati atleta: {e}")
        return None, None

def _estrai_valore(df, etichetta):
    for _, row in df.iterrows():
        if str(row[0]).strip().lower() == etichetta.lower():
            return row[1] if len(row) > 1 else None
    return None

def carica_lattato(nome, tecnica):
    """Estrae i valori di lattato da un foglio."""
    try:
        df = pd.read_excel(f"data/{nome}.xlsx", sheet_name=tecnica, header=None)
        idx = df[df.iloc[:, 0].astype(str).str.contains("lattato", case=False)].index
        if not idx.empty:
            r = idx[0]
            titoli = df.iloc[r - 1, 1:].tolist()
            valori = df.iloc[r, 1:].tolist()
            return titoli, valori
        return [], []
    except:
        return [], []

def carica_split_segmenti(nome, tecnica):
    """Carica i dati di split segmenti da una tabella (dopo riga 20)."""
    try:
        df = pd.read_excel(f"data/{nome}.xlsx", sheet_name=tecnica, skiprows=20, usecols="A:F")
        return df.dropna(how="all")
    except:
        return pd.DataFrame()
