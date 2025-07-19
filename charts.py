# charts.py
import plotly.express as px
import pandas as pd

class GenerateViz:
    @staticmethod
    def plot_stats_keywords(df):
        """
        df attendu : colonnes ['keyword', 'count']
        """
        try:
            df_sorted = df.sort_values("count", ascending=True).tail(15)
            fig = px.bar(
                df_sorted,
                x="count",
                y="keyword",
                orientation="h",
                title="🔑 Mots-clés les plus fréquents",
                labels={"count": "Occurrences", "keyword": "Mot-clé"}
            )
            return fig
        except Exception as e:
            print(f"Erreur génération mots-clés: {e}")
            return None

    @staticmethod
    def plot_stats_domains(df):
        """
        df attendu : colonnes ['domain', 'count']
        """
        try:
            fig = px.pie(
                df,
                names="domain",
                values="count",
                title="📚 Répartition par domaine"
            )
            return fig
        except Exception as e:
            print(f"Erreur génération domaines: {e}")
            return None

    @staticmethod
    def plot_articles_by_year(df):
        """
        df attendu : colonnes ['year', 'count']
        """
        try:
            df_sorted = df.sort_values("year")
            fig = px.line(
                df_sorted,
                x="year",
                y="count",
                title="📈 Évolution des publications par année",
                labels={"count": "Nombre de publications", "year": "Année"}
            )
            fig.update_layout(plot_bgcolor='white')
            return fig
        except Exception as e:
            print(f"Erreur génération articles/année: {e}")
            return None

    @staticmethod
    def plot_top_authors(df, top=10):
        """
        df attendu : colonnes ['author', 'count']
        """
        try:
            df_sorted = df.sort_values("count", ascending=True).tail(top)
            fig = px.bar(
                df_sorted,
                x="count",
                y="author",
                orientation="h",
                title=f"👤 Top {top} auteurs",
                labels={"count": "Publications", "author": "Auteur"}
            )
            return fig
        except Exception as e:
            print(f"Erreur génération top auteurs: {e}")
            return None

    @staticmethod
    def plot_articles_by_word(df, keyword):
        """
        df attendu : colonnes ['year', 'count']
        """
        try:
            df_sorted = df.sort_values("year")
            fig = px.bar(
                df_sorted,
                x="year",
                y="count",
                title=f"📚 Publications avec le mot-clé '{keyword}' par année",
                labels={"count": "Nombre", "year": "Année"}
            )
            return fig
        except Exception as e:
            print(f"Erreur génération par mot-clé '{keyword}': {e}")
            return None
