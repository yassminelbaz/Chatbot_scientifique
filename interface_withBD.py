import os
os.environ["USE_TF"] = "0"

import faiss
import numpy as np
import mysql.connector
import streamlit as st
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from charts import GenerateViz
import pandas as pd

# Charger .env
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Chargement des ressources
@st.cache_resource
def load_resources():
    index = faiss.read_index("faiss_index_articles1.index")
    article_ids = np.load("indexed_article_ids.npy", allow_pickle=True)
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return index, article_ids, model

index, article_ids, model = load_resources()

# Connexion BDD
def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# Obtenir les options de filtres
@st.cache_data
def get_filter_options():
    conn = get_connection()
    cursor = conn.cursor()

    # Récupérer les années disponibles dans la table articles
    cursor.execute("SELECT DISTINCT year FROM articles WHERE year IS NOT NULL ORDER BY year DESC")
    years = [row[0] for row in cursor.fetchall()]

    # Récupérer les auteurs ayant au moins un article associé
    cursor.execute("""
        SELECT DISTINCT au.author
        FROM authors au
        JOIN article_author aa ON au.author_id = aa.author_id
        JOIN articles a ON aa.id_article = a.id_article
        ORDER BY au.author ASC
    """)
    authors = [row[0] for row in cursor.fetchall()]

    # Récupérer les domaines renseignés dans la table articles
    cursor.execute("SELECT DISTINCT domain FROM articles WHERE domain IS NOT NULL AND domain != '' ORDER BY domain ASC")
    domains = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return years, authors, domains

# Fonction de recherche
def search_semantically(query, year_filter, author_filter, domain_filter, k=5):
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, k)
    ids_articles = [article_ids[i] for i in indices[0]]

    if not ids_articles:
        return []

    placeholders = ','.join(['%s'] * len(ids_articles))
    filters = []

    if year_filter and year_filter != "Tous":
        filters.append(f"a.year = '{year_filter}'")
    if author_filter and author_filter != "Tous":
        filters.append(f"au.author = '{author_filter}'")
    if domain_filter and domain_filter != "Tous":
        filters.append(f"a.domain = '{domain_filter}'")

    where_clause = f"WHERE a.id_article IN ({placeholders})"
    if filters:
        where_clause += " AND " + " AND ".join(filters)

    sql = f"""
        SELECT a.id_article, a.title, a.abstract, a.year, a.doi, a.domain,
               GROUP_CONCAT(au.author SEPARATOR ', ') AS authors
        FROM articles a
        LEFT JOIN article_author aa ON a.id_article = aa.id_article
        LEFT JOIN authors au ON aa.author_id = au.author_id
        {where_clause}
        GROUP BY a.id_article
        ORDER BY FIELD(a.id_article, {','.join(['%s']*len(ids_articles))})
    """

    params = ids_articles + ids_articles
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, params)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

# ========================
#   INTERFACE STREAMLIT
# ========================
st.set_page_config(page_title="Chatbot Scientifique", layout="wide")

# CSS custom
st.markdown("""
<style>
.user-message {
    background-color: #e3f2fd;
    padding: 12px 16px;
    border-radius: 18px 18px 0 18px;
    margin: 8px 0;
    margin-left: auto;
    max-width: 80%;
}
.bot-message {
    background-color: #f5f5f5;
    padding: 12px 16px;
    border-radius: 18px 18px 18px 0;
    margin: 8px 0;
    margin-right: auto;
    max-width: 80%;
}
.paper-card {
    background-color: white;
    padding: 12px;
    margin: 8px 0;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

st.title("💬 Chatbot Scientifique ArXiv")

if 'history' not in st.session_state:
    st.session_state.history = []
if 'last_query' not in st.session_state:
    st.session_state.last_query = None

# Sidebar
st.sidebar.header("🔍 Filtres de recherche")
years, authors, domains = get_filter_options()
selected_year = st.sidebar.selectbox("Année", ["Tous"] + years)
selected_author = st.sidebar.selectbox("Auteur", ["Tous"] + authors)
selected_domain = st.sidebar.selectbox("Domaine", ["Tous"] + domains)

# Chat container
chat_container = st.container()
with chat_container:
    for msg, is_user in st.session_state.history:
        style = "user-message" if is_user else "bot-message"
        st.markdown(f"<div class='{style}'>{msg}</div>", unsafe_allow_html=True)

# Input
query = st.text_input("Posez votre question scientifique...")

if query and query != st.session_state.last_query:
    st.session_state.last_query = query
    st.session_state.history.append((query, True))  # Message utilisateur

    with st.spinner("🔍 Recherche en cours..."):
        conn = get_connection()

        if "mot-clé" in query.lower() or "keywords" in query.lower():
            df = pd.read_sql("""
                SELECT k.keyword AS keywords
                FROM article_keyword ak
                JOIN keywords k ON ak.keyword_id = k.keyword_id
            """, conn)
            fig = GenerateViz.plot_stats_keywords(df)
            if fig: st.plotly_chart(fig, use_container_width=True)

        elif "domaine" in query.lower():
            df = pd.read_sql("SELECT domain FROM articles", conn)
            fig = GenerateViz.plot_stats_domains(df)
            if fig: st.plotly_chart(fig, use_container_width=True)

        elif "année" in query.lower() or "évolution" in query.lower():
            df = pd.read_sql("SELECT year FROM articles", conn)
            fig = GenerateViz.plot_articles_by_year(df)
            if fig: st.plotly_chart(fig, use_container_width=True)

        elif "auteur" in query.lower():
            df = pd.read_sql("""
                SELECT GROUP_CONCAT(au.author SEPARATOR ';') AS authors
                FROM article_author aa
                JOIN authors au ON aa.author_id = au.author_id
                GROUP BY aa.id_article
            """, conn)
            fig = GenerateViz.plot_top_authors(df)
            if fig: st.plotly_chart(fig, use_container_width=True)

        else:
            results = search_semantically(
            query,
            year_filter=selected_year,
            author_filter=selected_author,
            domain_filter=selected_domain,
            k=10
        )

    if results:
        response = ["Voici les publications pertinentes :"]
        for res in results:
            card = f"""
            <div class='paper-card'>
                <div class='paper-title'><strong>{res['title']}</strong></div>
                <div><b>👤 Auteurs :</b> {res['authors']}</div>
                <div><b>📅 Année :</b> {res['year']} | <b>🏷️ Domaine :</b> {res['domain'] or 'N/A'}</div>
                <div><b>🔗 DOI :</b> {res['doi'] or 'Non disponible'}</div>
                <div>{res['abstract'][:500]}...</div>
            </div>
            """
            response.append(card)
        st.session_state.history.append(("<br>".join(response), False))
    else:
        st.session_state.history.append(("Je n'ai trouvé aucune publication correspondant à votre recherche.", False))
    conn.close()
st.rerun()
