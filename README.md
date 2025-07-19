Guide d'Installation et Utilisation du Chatbot Scientifique

📝 Description du Projet

Ce projet consiste en un chatbot intelligent capable d'interagir avec les utilisateurs pour répondre à des questions sur des publications scientifiques issues de la base de données Arxiv. Le chatbot utilise des techniques de NLP et d'indexation sémantique pour fournir des réponses pertinentes.

⚙️ Prérequis

Python 3.8 ou supérieur

MySQL Server

📦 Installation

1. Cloner le dépôt
   git clone [URL_DU_DEPOT]
   cd [NOM_DU_DEPOT]

2. Créer un environnement virtuel (recommandé)
   python -m venv venv
   source venv/bin/activate # Sur Linux/Mac
   venv\Scripts\activate # Sur Windows

3. Installer les dépendances
   pip install streamlit mysql-connector-python pandas numpy sentence-transformers faiss-cpu plotly python-dotenv spacy
   python -m spacy download en_core_web_sm

4. Configuration de la base de données
   a-Créez une base de données MySQL en exécutant le script CreationBD.sql
   b-Configurez les variables d'environnement dans un fichier .env :
   DB_HOST=localhost
   DB_USER=votre_utilisateur
   DB_PASSWORD=votre_mot_de_passe
   DB_NAME=chatbot_db

🚀 Lancement de l'application

streamlit run interface_withBD.py

🛠 Structure des fichiers

=> CreationBD.sql : Script SQL pour créer la structure de la base de données

=> charts.py : Module de visualisation des données

=> intent_detector.py : Détection d'intention avec NLP

=> interface_withBD.py : Interface Streamlit principale

=> vectorisation.ipynb : Notebook pour la vectorisation des données et création de l'index FAISS

=> InsertionDesDonnées.ipynb : Notebook pour l'importation des données dans MySQL

🤖 Utilisation

=> Lancez l'application avec streamlit run interface_withBD.py

=> Posez votre question dans la zone de texte (ex: "Quelles sont les publications récentes sur l'apprentissage automatique?")

=> Utilisez les filtres dans la sidebar pour affiner votre recherche

=> Consultez les résultats et visualisations générés

📚 Données gérées

Le système gère les données suivantes :

=> Articles (titre, résumé, année, DOI, domaine)

=> Auteurs

=> Mots-clés

📌 Note importante sur l'organisation des fichiers :

Pour garantir le bon fonctionnement de l'application, tous les données fournis (les fichiers CSV) doivent impérativement être placés dans le même dossier racine. L'application utilise des chemins relatifs simples (uniquement les noms de fichiers), ce qui signifie qu'elle cherche automatiquement ces fichiers dans le dossier où elle est exécutée. Aucune modification de chemin n'est nécessaire, mais un mauvais placement des fichiers entraînera des erreurs.
