from typing import List, Dict
import re
import logging

class EntityClassifier:
    def __init__(self, config=None):  # Aggiungi parametro config
        self.config = config
        self.entities = []
        self.logger = logging.getLogger(__name__)

    async def classify_entities(self, results: List[Dict]) -> List[Dict]:  # Cambia signature
        """Classifica le entità per ogni pagina analizzata"""
        classified_results = []
        
        for page_data in results:
            if not page_data:
                continue
                
            # Estrai entità dal contenuto testuale
            entities = self._extract_entities(page_data.get('text_content', ''))
            
            # Aggiungi le entità classificate ai dati della pagina
            page_data['entities'] = entities
            classified_results.append(page_data)
            
        return classified_results
    
    def _extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Estrae entità dal testo usando pattern regex"""
        entities = {
            'emails': self._extract_emails(text),
            'phones': self._extract_phones(text),
            'urls': self._extract_urls(text),
            'organizations': self._extract_organizations(text)
        }
        return entities
    
    def _extract_emails(self, text: str) -> List[str]:
        """Estrae indirizzi email"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return list(set(re.findall(email_pattern, text)))
    
    def _extract_phones(self, text: str) -> List[str]:
        """Estrae numeri di telefono"""
        phone_pattern = r'\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b'
        return list(set(re.findall(phone_pattern, text)))
    
    def _extract_urls(self, text: str) -> List[str]:
        """Estrae URL dal testo"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return list(set(re.findall(url_pattern, text)))
    
    def _extract_organizations(self, text: str) -> List[str]:
        """Estrae nomi di organizzazioni (pattern semplificato)"""
        # Pattern basilare per organizzazioni (parole capitalizzate seguite da Inc, LLC, etc.)
        org_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Inc|LLC|Corp|Ltd|Company)\b'
        return list(set(re.findall(org_pattern, text)))