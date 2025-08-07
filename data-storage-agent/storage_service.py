import pandas as pd
import os
import json
from datetime import datetime
from typing import Dict, Any, List
import logging

class DataStorageService:
    def __init__(self, config):
        self.config = config
        self.data_path = config['database']['data_path']
        os.makedirs(self.data_path, exist_ok=True)
        self.logger = logging.getLogger(__name__)
        
    async def store_analysis(self, task_id: str, search_results: Dict, analyzed_content: Dict) -> Dict:
        """Memorizza i risultati dell'analisi in formato pandas"""
        try:
            # Prepara i dati per il DataFrame
            records = []
            pages = analyzed_content.get('pages', [])
            
            for page in pages:
                if page:  # Verifica che la pagina non sia None
                    record = {
                        'task_id': task_id,
                        'timestamp': datetime.now().isoformat(),
                        'url': page.get('url', ''),
                        'title': page.get('title', ''),
                        'description': page.get('description', ''),
                        'keywords': json.dumps(page.get('keywords', [])),
                        'headings_h1': json.dumps(page.get('headings', {}).get('h1', [])),
                        'headings_h2': json.dumps(page.get('headings', {}).get('h2', [])),
                        'headings_h3': json.dumps(page.get('headings', {}).get('h3', [])),
                        'links_count': page.get('links_count', 0),
                        'images_count': page.get('images_count', 0),
                        'word_count': page.get('word_count', 0),
                        'language': page.get('language', 'unknown'),
                        'search_affinity_score': page.get('original_search_score', 0.0),
                        'text_preview': page.get('text_content', '')[:500]  # Prime 500 caratteri
                    }
                    records.append(record)
            
            if not records:
                raise ValueError("Nessun dato valido da memorizzare")
            
            # Crea DataFrame
            df = pd.DataFrame(records)
            
            # Salva come CSV e Pickle per performance
            csv_path = os.path.join(self.data_path, f"{task_id}.csv")
            pickle_path = os.path.join(self.data_path, f"{task_id}.pkl")
            
            df.to_csv(csv_path, index=False, encoding='utf-8')
            df.to_pickle(pickle_path)
            
            # Backup se abilitato
            if self.config['database'].get('backup_enabled', False):
                backup_path = os.path.join(self.data_path, 'backups')
                os.makedirs(backup_path, exist_ok=True)
                df.to_csv(os.path.join(backup_path, f"{task_id}_backup.csv"), index=False)
            
            # Aggiorna il registro delle attività
            await self._update_task_registry(task_id, len(records))
            
            return {
                'success': True,
                'file_path': csv_path,
                'records_count': len(records)
            }
            
        except Exception as e:
            self.logger.error(f"Storage error for task {task_id}: {e}")
            raise e
    
    async def get_task_data(self, task_id: str) -> Dict:
        """Recupera i dati di un task specifico"""
        pickle_path = os.path.join(self.data_path, f"{task_id}.pkl")
        csv_path = os.path.join(self.data_path, f"{task_id}.csv")
        
        try:
            if os.path.exists(pickle_path):
                df = pd.read_pickle(pickle_path)
            elif os.path.exists(csv_path):
                df = pd.read_csv(csv_path)
            else:
                raise FileNotFoundError(f"Dati non trovati per task {task_id}")
            
            return {
                'task_id': task_id,
                'records_count': len(df),
                'data': df.to_dict('records'),
                'summary': {
                    'unique_domains': df['url'].apply(lambda x: x.split('/')[2] if '/' in x else x).nunique(),
                    'avg_word_count': df['word_count'].mean(),
                    'languages': df['language'].value_counts().to_dict(),
                    'top_scoring_pages': df.nlargest(5, 'search_affinity_score')[['url', 'title', 'search_affinity_score']].to_dict('records')
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error retrieving task {task_id}: {e}")
            raise e
    
    async def _update_task_registry(self, task_id: str, records_count: int):
        """Aggiorna il registro delle attività"""
        registry_path = os.path.join(self.data_path, 'task_registry.json')
        
        try:
            if os.path.exists(registry_path):
                with open(registry_path, 'r') as f:
                    registry = json.load(f)
            else:
                registry = {}
            
            registry[task_id] = {
                'timestamp': datetime.now().isoformat(),
                'records_count': records_count,
                'status': 'completed'
            }
            
            with open(registry_path, 'w') as f:
                json.dump(registry, f, indent=2)
                
        except Exception as e:
            self.logger.warning(f"Could not update task registry: {e}")