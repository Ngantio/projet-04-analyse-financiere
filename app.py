# ============================================================
# PROJET 4 — DASHBOARD FINANCIER INTERACTIF
# Stack : Streamlit, yfinance, Plotly
# ============================================================

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="Dashboard Financier",
    page_icon="📈",
    layout="wide"
)

# --- Portefeuille disponible ---
TICKERS = {
    'AAPL': 'Apple',
    'MSFT': 'Microsoft',
    'TSLA': 'Tesla',
    'EZA': 'ETF Afrique du Sud',
    'NPN.JO': 'Naspers (JSE)'
}

@st.cache_data
def charger_donnees(tickers_selectionnes, date_debut, date_fin):
    data = {}
    for symbole in tickers_selectionnes:
        try:
            hist = yf.download(symbole, start=date_debut, end=date_fin, progress=False)
            if not hist.empty:
                close = hist['Close']
                if isinstance(close, pd.DataFrame):
                    close = close.iloc[:, 0]
                data[symbole] = close
        except Exception:
            pass
    
    prix = pd.DataFrame(data)
    prix = prix.ffill().dropna()
    return prix

# --- Titre ---
st.title("📈 Dashboard d'Analyse Financière")
st.markdown("**Portefeuille mixte** — Valeurs internationales + exposition africaine (JSE)")
st.divider()

# --- Sidebar ---
st.sidebar.header("🔧 Paramètres")

actifs_selectionnes = st.sidebar.multiselect(
    "Sélectionner les actifs",
    options=list(TICKERS.keys()),
    default=list(TICKERS.keys()),
    format_func=lambda x: f"{x} — {TICKERS[x]}"
)

date_debut = st.sidebar.date_input("Date de début", value=pd.to_datetime("2022-01-01"))
date_fin = st.sidebar.date_input("Date de fin", value=pd.to_datetime("2024-12-31"))

taux_sans_risque = st.sidebar.slider(
    "Taux sans risque annuel (%)", 
    min_value=0.0, max_value=10.0, value=4.0, step=0.5
) / 100

if not actifs_selectionnes:
    st.warning("⚠️ Sélectionne au moins un actif dans la sidebar.")
    st.stop()

# --- Chargement ---
with st.spinner("Téléchargement des données..."):
    prix = charger_donnees(actifs_selectionnes, date_debut, date_fin)

if prix.empty:
    st.error("❌ Aucune donnée récupérée. Vérifie les tickers ou la période.")
    st.stop()

log_returns = np.log(prix / prix.shift(1)).dropna()

# ============================================================
# KPIs
# ============================================================

rendement_annuel = log_returns.mean() * 252
volatilite_annuelle = log_returns.std() * np.sqrt(252)
sharpe_ratio = (rendement_annuel - taux_sans_risque) / volatilite_annuelle

st.subheader("📊 Résumé risque/rendement")

resume = pd.DataFrame({
    'Rendement annuel': (rendement_annuel * 100).round(1).astype(str) + '%',
    'Volatilité annuelle': (volatilite_annuelle * 100).round(1).astype(str) + '%',
    'Sharpe Ratio': sharpe_ratio.round(3)
}).sort_values('Sharpe Ratio', ascending=False)

st.dataframe(resume, use_container_width=True)

st.divider()

# ============================================================
# GRAPHIQUE 1 — Performance cumulée
# ============================================================

st.subheader("📈 Performance cumulée (base 100)")

performance_cumulee = (prix / prix.iloc[0]) * 100

fig1 = go.Figure()
for colonne in performance_cumulee.columns:
    fig1.add_trace(go.Scatter(
        x=performance_cumulee.index,
        y=performance_cumulee[colonne],
        mode='lines',
        name=colonne
    ))
fig1.add_hline(y=100, line_dash="dash", line_color="gray")
fig1.update_layout(
    xaxis_title="Date",
    yaxis_title="Valeur (base 100)",
    hovermode='x unified',
    height=500
)
st.plotly_chart(fig1, use_container_width=True)

st.divider()

# ============================================================
# GRAPHIQUE 2 — Volatilité glissante
# ============================================================

st.subheader("📉 Volatilité glissante annualisée (30 jours)")

volatilite_glissante = log_returns.rolling(window=30).std() * np.sqrt(252)

fig2 = go.Figure()
for colonne in volatilite_glissante.columns:
    fig2.add_trace(go.Scatter(
        x=volatilite_glissante.index,
        y=volatilite_glissante[colonne],
        mode='lines',
        name=colonne
    ))
fig2.update_layout(
    xaxis_title="Date",
    yaxis_title="Volatilité annualisée",
    yaxis_tickformat=".0%",
    hovermode='x unified',
    height=450
)
st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ============================================================
# GRAPHIQUE 3 — Matrice de corrélation
# ============================================================

st.subheader("🔗 Corrélation entre les rendements")

correlation = log_returns.corr()

fig3 = go.Figure(data=go.Heatmap(
    z=correlation.values,
    x=correlation.columns,
    y=correlation.columns,
    colorscale='RdBu',
    zmid=0,
    text=correlation.round(2).values,
    texttemplate="%{text}"
))
fig3.update_layout(height=450)
st.plotly_chart(fig3, use_container_width=True)

st.divider()
st.markdown("**Shanice Marvin Tiogang** · Data Science Portfolio · 2026")