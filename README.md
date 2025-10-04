# Tableau de Bord Boutique Algérie

Application Streamlit pour analyser les ventes d'une boutique algérienne.

## Quick Start

```bash
pip install streamlit pandas plotly
streamlit run streamlit.py
```

## Fichiers

- `streamlit.py` - Application principale
- `create_database.py` - Crée la base de données
- `Ventes_Boutique.db` - Base SQLite (auto-générée)



## Captures d'Écran

### Tableau de Bord Principal
![Dashboard](screenshots/1.png)

### CA par Wilaya  
![Wilayas](screenshots/3.png)

### Évolution Mensuelle
![Evolution](screenshots/4.png)

### Détail des Ventes
![Top 10 produits](screenshots/2.png)


## Fonctionnalités

- Chiffre d'affaires total & quantité vendue
- CA par wilaya algérienne  
- Top 10 produits
- Évolution mensuelle du CA
- Filtres date + wilaya

## Métriques

- **CA Total** - Somme des ventes en DA
- **Quantité Vendue** - Unités vendues
- **Panier Moyen** - CA par transaction
- **Top Produits** - Classement par performance

---

*Développé avec Streamlit + SQLite*