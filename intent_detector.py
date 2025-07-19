# intent_detector.py

import spacy
from spacy.matcher import PhraseMatcher

class IntentDetector:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        
        self.patterns = {
            "year_stats": [
                "année", "années", "évolution", "historique", "nombre d'articles",
        "year", "years", "trend", "evolution", "publications par année",
        "count by year", "annual publications", "nombre publications"
            ],
            "author_stats": [
                "auteur", "auteurs", "productivité", "contribution",
                "author", "authors", "productivity"
            ],
            "domain_stats": [
                "domaine", "domaines", "sujet", "thématique",
                "domain", "field", "subject", "topic"
            ],
            "keyword_stats": [
                "mot-clé", "mots-clés", "terminologie",
                "keyword", "keywords", "terms"
            ],
            "publication_trend": ["tendance", "évolution", "trend", "historique"],
            "author_network": ["auteurs", "collaboration", "réseau", "network"],
            "domain_distribution": ["domaines", "répartition", "distribution", "sujets"]
        }
        
        self._setup_matcher()
    
    def _setup_matcher(self):
        for intent, patterns in self.patterns.items():
            self.matcher.add(intent, [self.nlp(text) for text in patterns])
    
    def detect_intent(self, text):
        doc = self.nlp(text.lower())
        matches = self.matcher(doc)
        if matches:
            return self.nlp.vocab.strings[matches[0][0]]
        return None
