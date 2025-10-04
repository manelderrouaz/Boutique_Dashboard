import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Configuration de la page
st.set_page_config(
    page_title="Tableau de Bord - Boutique",
    page_icon="🇩🇿",
    layout="wide"
)

# Titre de l'application
st.title("🇩🇿 Tableau de Bord - Boutique Algérienne")
st.markdown("---")

def get_connection():
    return sqlite3.connect('Ventes_Boutique.db') 

# Fonction pour récupérer les données des ventes avec jointures
def get_ventes_completes():
    conn = get_connection()
    query = '''
        SELECT 
            v.*,
            c.nom as client_nom,
            c.wilaya,
            p.nom as produit_nom,
            p.categorie,
            p.prix
        FROM ventes v
        JOIN clients c ON v.client_id = c.id
        JOIN produits p ON v.produit_id = p.id
    '''
    df = pd.read_sql(query, conn)
    conn.close()
    
    # Conversion des dates
    df['date_vente'] = pd.to_datetime(df['date_vente'])
    
    return df

# Chargement des données
@st.cache_data
def load_data():
    return get_ventes_completes()

# Sidebar pour les filtres
st.sidebar.title("Filtres")

# Charger les données
ventes_df = load_data()

# Filtre par date
st.sidebar.subheader("Filtre Temporel")
date_min = ventes_df['date_vente'].min().date()
date_max = ventes_df['date_vente'].max().date()

date_debut = st.sidebar.date_input(
    "Date de début",
    value=date_max - timedelta(days=90),
    min_value=date_min,
    max_value=date_max
)

date_fin = st.sidebar.date_input(
    "Date de fin",
    value=date_max,
    min_value=date_min,
    max_value=date_max
)

# Filtre par wilaya
wilayas = ['Toutes'] + sorted(ventes_df['wilaya'].unique())
wilaya_selectionnee = st.sidebar.selectbox("Wilaya", wilayas)

# Application des filtres
ventes_filtrees = ventes_df[
    (ventes_df['date_vente'].dt.date >= date_debut) & 
    (ventes_df['date_vente'].dt.date <= date_fin)
]

if wilaya_selectionnee != 'Toutes':
    ventes_filtrees = ventes_filtrees[ventes_filtrees['wilaya'] == wilaya_selectionnee]


# Section 1: Métriques principales
st.header("Métriques Clés")

col1, col2, col3, col4 = st.columns(4)

with col1:
    ca_total = ventes_filtrees['montant_total'].sum()
    st.metric(
        "Chiffre d'Affaires Total", 
        f"{ca_total:,.0f} DA",
        help="Somme totale des ventes en Dinars Algériens"
    )

with col2:
    quantite_totale = ventes_filtrees['quantite'].sum()
    st.metric(
        "Quantité Totale Vendue", 
        f"{quantite_totale:,} unités",
        help="Nombre total de produits vendus"
    )

with col3:
    nb_ventes = len(ventes_filtrees)
    st.metric(
        "Nombre de Ventes", 
        f"{nb_ventes:,}",
        help="Nombre total de transactions"
    )

with col4:
    panier_moyen = ca_total / nb_ventes if nb_ventes > 0 else 0
    st.metric(
        "Panier Moyen", 
        f"{panier_moyen:,.0f} DA",
        help="Chiffre d'affaires moyen par vente"
    )

st.markdown("---")


# Section 2: Graphiques
st.header("Analyses Géographiques et Produits")

col1, col2 = st.columns(2)

with col1:
    st.subheader("CA par Wilaya")
    
    # Calcul du CA par wilaya
    ca_wilaya = ventes_filtrees.groupby('wilaya')['montant_total'].sum().reset_index()
    ca_wilaya = ca_wilaya.sort_values('montant_total', ascending=False)
    
    if not ca_wilaya.empty:
        fig_wilaya = px.bar(
            ca_wilaya,
            x='montant_total',
            y='wilaya',
            orientation='h',
            title=f"Chiffre d'Affaires par Wilaya ({date_debut} à {date_fin})",
            labels={'montant_total': 'CA (DA)', 'wilaya': 'Wilaya'},
            color='montant_total',
            color_continuous_scale='viridis'
        )
        fig_wilaya.update_layout(showlegend=False)
        st.plotly_chart(fig_wilaya, use_container_width=True)
    else:
        st.info("Aucune donnée disponible pour les filtres sélectionnés")

with col2:
    st.subheader("Top 10 des Produits")
    
    # Calcul des top produits par CA
    top_produits_ca = ventes_filtrees.groupby('produit_nom')['montant_total'].sum().nlargest(10).reset_index()
    
    if not top_produits_ca.empty:
        fig_top_produits = px.pie(
            top_produits_ca,
            values='montant_total',
            names='produit_nom',
            title="Top 10 Produits par Chiffre d'Affaires",
            hole=0.4
        )
        fig_top_produits.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_top_produits, use_container_width=True)
    else:
        st.info("Aucune donnée disponible pour les filtres sélectionnés")

# Section 3: Évolution mensuelle du CA
st.markdown("---")
st.header("Évolution Mensuelle du Chiffre d'Affaires")

# Préparation des données pour l'évolution mensuelle
ventes_filtrees['mois_annee'] = ventes_filtrees['date_vente'].dt.to_period('M').astype(str)
evolution_mensuelle = ventes_filtrees.groupby('mois_annee')['montant_total'].sum().reset_index()

if not evolution_mensuelle.empty:
    fig_evolution = px.line(
        evolution_mensuelle,
        x='mois_annee',
        y='montant_total',
        title="Évolution Mensuelle du Chiffre d'Affaires",
        labels={'mois_annee': 'Mois', 'montant_total': 'CA (DA)'},
        markers=True
    )
    
    fig_evolution.update_layout(
        xaxis_title="Mois",
        yaxis_title="Chiffre d'Affaires (DA)",
        hovermode='x unified'
    )
    
    # Ajouter une courbe de tendance
    if len(evolution_mensuelle) > 1:
        fig_evolution.add_trace(
            go.Scatter(
                x=evolution_mensuelle['mois_annee'],
                y=evolution_mensuelle['montant_total'].rolling(window=2, min_periods=1).mean(),
                mode='lines',
                line=dict(dash='dash', color='orange'),
                name='Tendance'
            )
        )
    
    st.plotly_chart(fig_evolution, use_container_width=True)
else:
    st.info("Aucune donnée disponible pour l'évolution mensuelle avec les filtres sélectionnés")

# Bouton de rafraîchissement dans la sidebar
with st.sidebar:
    st.markdown("---")
    if st.button("🔄 Rafraîchir les Données"):
        st.cache_data.clear()
        st.rerun() 