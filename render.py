
import streamlit as st
import plotly.graph_objects as go

def mostra_metrica(col, label, valore, simbolo, unit):
    display = f"<div style='font-size: 32px;'> {simbolo} {label}: <strong>{valore:.1f} {unit}</strong></div>" if valore else f"<div style='font-size: 32px;'> {simbolo} {label}: N/D</div>"
    col.markdown(display, unsafe_allow_html=True)

def mostra_segmenti(df):
    col_sx, col_dx = st.columns([1, 3])
    with col_sx:
        st.subheader("📏 Segmenti")
        for i, row in df.iterrows():
            st.markdown(f"""
                <div style='margin-bottom: 8px; padding: 10px 14px; background-color: #eeeeee; border-radius: 8px;'>
                    <strong>📍 {i}</strong><br>
                    📏 {row['lunghezza (m)']:.1f} m<br>
                    ⛰️ {row['dislivello (m)']:.1f} m<br>
                    📉 {row['pendenza media (%)']:.1f} %
                </div>
            """, unsafe_allow_html=True)
    with col_dx:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[0] + df['lunghezza (m)'].cumsum().tolist(),
            y=[0] + df['dislivello (m)'].cumsum().tolist(),
            mode="lines+markers"
        ))
        fig.update_layout(title="Profilo Altimetrico", xaxis_title="Distanza (m)", yaxis_title="Dislivello (m)")
        st.plotly_chart(fig, use_container_width=True)

def mostra_performance_box(df):
    etichette = [
        "Durata", "Velocità media (Km/h)", "Velocità max (Km/h)", 
        "VAM media (m/h)", "HR max", "HR media", "HR media recupero"
    ]
    col1, col2, col3 = st.columns(3)
    for i, et in enumerate(etichette):
        val = df[df[0].str.lower() == et.lower()][1].values[0]
        col = [col1, col2, col3][i % 3]
        col.markdown(f"<div style='padding: 10px; background: #eeeeee; border-radius: 10px;'><b>{et}</b><br>{val}</div>", unsafe_allow_html=True)

def mostra_lattato(nome, tecnica):
    from utils.data_loader import carica_lattato
    titoli, valori = carica_lattato(nome, tecnica)
    if not valori: return st.warning("Nessun dato lattato trovato.")
    st.subheader("Valori Lattato (mmol/l)")
    cols = st.columns(len(valori))
    for i in range(len(valori)):
        with cols[i]:
            st.markdown(f"<div style='text-align:center; background:#eee; padding:10px; border-radius:6px'><b>{titoli[i]}</b><br>{float(valori[i]):.1f}</div>", unsafe_allow_html=True)

def mostra_split_segmenti(nome, tecnica):
    from utils.data_loader import carica_split_segmenti
    df = carica_split_segmenti(nome, tecnica)
    if df.empty:
        st.warning("Nessun dato Split Segmenti.")
        return
    df.columns = [
        "Segmento", "Durata (s)", "Vel_media (km/h)", "Vam_media (m/h)", 
        "Cadenza media (passi/min)", "Lunghezza passo media (m)"
    ]
    for _, row in df.iterrows():
        st.markdown(f"<hr><strong>📍 {row['Segmento']}</strong>", unsafe_allow_html=True)
        cols = st.columns(5)
        for i, label in enumerate(df.columns[1:]):
            with cols[i]:
                val = float(str(row[label]).replace(',', '.'))
                st.markdown(f"<div>{label}<br><b>{val:.2f}</b></div>", unsafe_allow_html=True)
