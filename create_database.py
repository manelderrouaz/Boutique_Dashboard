import sqlite3
import random
from datetime import datetime, timedelta

def create_database():
    #creation de la base de données 
    conn = sqlite3.connect('Ventes_Boutique.db')
    cursor = conn.cursor()
    
    # création de le table clients 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            email TEXT NOT NULL,
            wilaya TEXT NOT NULL,
            date_inscription DATE NOT NULL
        )
    ''')
    
    # création de la table produits
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            categorie TEXT NOT NULL,
            prix REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')
    
    # Création de la table ventes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ventes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            produit_id INTEGER NOT NULL,
            quantite INTEGER NOT NULL,
            date_vente DATE NOT NULL,
            montant_total REAL NOT NULL,
            FOREIGN KEY (client_id) REFERENCES clients (id),
            FOREIGN KEY (produit_id) REFERENCES produits (id)
        )
    ''')

    wilayas_algerie = [
        'Alger', 'Oran', 'Constantine', 'Annaba', 'Blida',
        'Batna', 'Sétif', 'Tlemcen', 'Béjaïa', 'Skikda',
        'Tizi Ouzou', 'Mostaganem', 'Msila', 'Djelfa', 'Sidi Bel Abbès'
    ]
    # Données fictives pour les clients
    clients = [
        ('Ahmed Benzema', 'ahmed@email.com', 'Alger', '2024-01-15'),
        ('Fatima Zohra', 'fatima@email.com', 'Oran', '2024-02-20'),
        ('Mohamed Bouchair', 'mohamed@email.com', 'Constantine', '2024-01-10'),
        ('Yasmine Kaci', 'yasmine@email.com', 'Annaba', '2024-03-05'),
        ('Karim Belkacem', 'karim@email.com', 'Blida', '2024-02-28'),
        ('Nadia Cherif', 'nadia@email.com', 'Batna', '2024-01-20'),
        ('Samir Boumediene', 'samir@email.com', 'Sétif', '2024-03-10'),
        ('Leila Messaoudi', 'leila@email.com', 'Tlemcen', '2024-02-15')
    ]
    
    cursor.executemany('''
        INSERT INTO clients (nom, email, wilaya, date_inscription)
        VALUES (?, ?, ?, ?)
    ''', clients)
    
    # Données fictives pour les produits
    produits = [
        ('Smartphone Samsung', 'Électronique', 45000.00, 15),
        ('Laptop Dell', 'Informatique', 85000.00, 10),
        ('Thé Céleste', 'Épicerie', 800.00, 50),
        ('Café Moulu', 'Épicerie', 1200.00, 30),
        ('Vêtement traditionnel', 'Mode', 5500.00, 20),
        ('Parfum', 'Beauté', 3500.00, 25),
        ('Dattes Deglet Nour', 'Épicerie', 2500.00, 40),
        ('Huile d\'Olive', 'Épicerie', 1800.00, 35),
        ('Smart TV LG', 'Électronique', 65000.00, 8),
        ('Couscoussier', 'Cuisine', 4200.00, 15)
    ]
    
    cursor.executemany('''
        INSERT INTO produits (nom, categorie, prix, stock)
        VALUES (?, ?, ?, ?)
    ''', produits)
    
    # Génération de ventes fictives
    ventes = []
    
    for _ in range(50):  # 50 ventes pour avoir plus de données
        client_id = random.randint(1, 8)
        produit_id = random.randint(1, 10)
        quantite = random.randint(1, 5)
        
        # Récupérer le prix du produit
        cursor.execute('SELECT prix FROM produits WHERE id = ?', (produit_id,))
        prix = cursor.fetchone()[0]
        montant_total = prix * quantite
        
        # Date aléatoire dans les 6 derniers mois
        date_vente = datetime.now() - timedelta(days=random.randint(1, 180))
        date_vente_str = date_vente.strftime('%Y-%m-%d')
        
        ventes.append((client_id, produit_id, quantite, date_vente_str, montant_total))
    
    cursor.executemany('''
        INSERT INTO ventes (client_id, produit_id, quantite, date_vente, montant_total)
        VALUES (?, ?, ?, ?, ?)
    ''', ventes)
    
    # Validation des changements et fermeture de la connexion
    conn.commit()
    conn.close()
    
    print("Base de données créée avec succès!")

if __name__ == "__main__":
    create_database()