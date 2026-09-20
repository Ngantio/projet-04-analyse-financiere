# Projet 4 — Analyse Financière & Marchés Boursiers 📈

##  Demo live
👉 [Accéder au dashboard](https://projet-04-analyse-financiere-mb4hamcfa5cppbczhynazm.streamlit.app/)

## Contexte
Analyse d'un portefeuille mixte combinant des valeurs technologiques internationales
et une exposition au marché sud-africain (JSE), pour évaluer le risque, le rendement
et la diversification à l'aide de métriques financières standards.

## Portefeuille analysé
| Ticker | Actif | Marché |
|---|---|---|
| AAPL | Apple | NASDAQ |
| MSFT | Microsoft | NASDAQ |
| TSLA | Tesla | NASDAQ |
| EZA | ETF Afrique du Sud (iShares MSCI) | NYSE Arca |
| NPN.JO | Naspers | Johannesburg Stock Exchange (JSE) |

**Période analysée :** Janvier 2022 – Décembre 2024

## Concepts financiers appliqués
- **Log-returns** — rendements logarithmiques (additifs dans le temps)
- **Rolling stats** — volatilité glissante annualisée (fenêtre 30 jours)
- **Corrélation** — matrice de corrélation entre les rendements quotidiens
- **Sharpe Ratio** — rendement ajusté au risque, vs taux sans risque
- **Performance cumulée** — indice base 100 pour comparaison multi-devises

## Insights clés
| # | Finding |
|---|---|
| 🏆 | Naspers (JSE) et Apple partagent le **meilleur Sharpe Ratio (0.269)** — deux profils opposés : rendement élevé/risque élevé vs rendement modéré/risque modéré |
| 📉 | Tesla affiche un **Sharpe Ratio négatif** malgré sa réputation — volatilité (60%) non compensée par le rendement sur la période |
| 🌍 | NPN.JO est **quasi-indépendant** des valeurs US (corrélation 0.16-0.19) — un vrai levier de diversification |
| 🔗 | AAPL-MSFT affichent la plus forte corrélation (0.69) — peu de diversification réelle entre les deux |

## Stack technique
![Python]
![yfinance]
![Streamlit]
![Plotly]

## Structure du repo
```
projet-04-analyse-financiere/
├── analyse_portefeuille.ipynb   — Analyse exploratoire complète
├── app.py                        — Dashboard Streamlit interactif
├── requirements.txt
└── README.md
```

## Note
Ce projet a servi de validation technique pour les métriques financières
(Sharpe ratio, volatilité, corrélation) destinées à [FinSight Africa](https://finsight-six-alpha.vercel.app/),
une plateforme d'analyse financière pour les marchés africains.

## Auteur
**Shanice Marvin Tiogang** · Business Analytics & Data Science · Tunis
