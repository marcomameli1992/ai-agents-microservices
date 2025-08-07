import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Dict
import logging
from urllib.parse import urljoin, urlparse
import re


class ContentAnalyzerService:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.session_timeout = aiohttp.ClientTimeout(total=30)
        
    async def analyze_pages(self, urls: List[Dict]) -> List[Dict]:
        """Analyzes the homepage of the search results."""
        semaphore = asyncio.Semaphore(self.config['ai_models']['max_concurrent_requests'])
        
        async with aiohttp.ClientSession(timeout=self.session_timeout) as session:
            tasks = [self._analyze_single_page(semaphore, session, url_data) 
                     for url_data in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter valid results
        valid_results = [r for r in results if isinstance(r, dict)]
        return valid_results
    
    async def _analyze_single_page(self, semaphore: asyncio.Semaphore, 
                                   session: aiohttp.ClientSession, 
                                   url_data: Dict) -> Dict:
        """Analyzes a single web page."""
        async with semaphore:
            try:
                url = url_data.get('href', '')
                if not url:
                    return None
                
                async with session.get(url) as response:
                    if response.status != 200:
                        return None
                    
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Extract structured information
                    analysis = {
                        'url': url,
                        'title': self._extract_title(soup),
                        'description': self._extract_description(soup),
                        'keywords': self._extract_keywords(soup),
                        'headings': self._extract_headings(soup),
                        'links_count': len(soup.find_all('a')),
                        'images_count': len(soup.find_all('img')),
                        'text_content': self._extract_clean_text(soup),
                        'word_count': 0,
                        'language': self._detect_language(soup),
                        'original_search_score': url_data.get('affinity_score', 0.0)
                    }
                    
                    analysis['word_count'] = len(analysis['text_content'].split())
                    return analysis
                    
            except Exception as e:
                self.logger.error(f"Error analyzing {url_data.get('href', 'unknown')}: {e}")
                return None
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extracts the page title."""
        title_tag = soup.find('title')
        return title_tag.get_text().strip() if title_tag else ""
    
    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extracts the meta description."""
        desc_tag = soup.find('meta', attrs={'name': 'description'})
        if desc_tag:
            return desc_tag.get('content', '').strip()
        return ""
    
    def _extract_keywords(self, soup: BeautifulSoup) -> List[str]:
        """Extracts the meta keywords."""
        keywords_tag = soup.find('meta', attrs={'name': 'keywords'})
        if keywords_tag:
            keywords = keywords_tag.get('content', '')
            return [k.strip() for k in keywords.split(',') if k.strip()]
        return []
    
    def _extract_headings(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """Extracts all headings (h1-h6)."""
        headings = {}
        for i in range(1, 7):
            h_tags = soup.find_all(f'h{i}')
            headings[f'h{i}'] = [h.get_text().strip() for h in h_tags]
        return headings
    
    def _extract_clean_text(self, soup: BeautifulSoup) -> str:
        """Extracts clean text from the page."""
        # Remove script and style
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        # Clean the text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text[:1000]  # Limit for performance
    
    def _detect_language(self, soup: BeautifulSoup) -> str:
        """Detects the language of the page."""
        html_tag = soup.find('html')
        if html_tag and html_tag.get('lang'):
            return html_tag.get('lang')
        return "unknown"