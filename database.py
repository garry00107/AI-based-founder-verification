# database.py
import json
import os
import logging
from datetime import datetime
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SearchDataStore:
    """Simple in-memory data store that works in serverless environments."""
    
    def __init__(self):
        self.searches = []
        self.cache_key = "founder_verification_searches"
    
    def add_search(self, search_data: Dict) -> bool:
        """Add a search record to the store."""
        try:
            # Add timestamp if not present
            if 'timestamp' not in search_data:
                search_data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Add unique ID
            search_data['id'] = len(self.searches) + 1
            
            self.searches.append(search_data)
            logging.info(f"Added search record for '{search_data.get('query', 'Unknown')}'")
            return True
        except Exception as e:
            logging.error(f"Error adding search record: {e}")
            return False
    
    def get_all_searches(self) -> List[Dict]:
        """Get all search records."""
        return self.searches.copy()
    
    def get_recent_searches(self, limit: int = 10) -> List[Dict]:
        """Get recent search records."""
        return self.searches[-limit:] if self.searches else []
    
    def get_stats(self) -> Dict:
        """Get statistics about searches."""
        total = len(self.searches)
        cache_hits = len([s for s in self.searches if s.get('cache_status') == 'HIT'])
        cache_misses = len([s for s in self.searches if s.get('cache_status') == 'MISS'])
        
        return {
            'total_searches': total,
            'cache_hits': cache_hits,
            'cache_misses': cache_misses,
            'cache_hit_rate': (cache_hits / total * 100) if total > 0 else 0
        }
    
    def export_to_csv_format(self) -> str:
        """Export data in CSV format."""
        if not self.searches:
            return ""
        
        # Get fieldnames from first record
        fieldnames = list(self.searches[0].keys())
        
        # Create CSV content
        csv_lines = [','.join(fieldnames)]
        for search in self.searches:
            row = []
            for field in fieldnames:
                value = str(search.get(field, ''))
                # Escape commas and quotes
                if ',' in value or '"' in value:
                    value = f'"{value.replace('"', '""')}"'
                row.append(value)
            csv_lines.append(','.join(row))
        
        return '\n'.join(csv_lines)

# Global instance
search_store = SearchDataStore()

# Alternative: Try to use Vercel KV if available
def get_vercel_kv_store():
    """Try to initialize Vercel KV store if available."""
    try:
        from vercel_kv import kv
        return kv
    except ImportError:
        logging.info("Vercel KV not available, using in-memory store")
        return None

def get_search_store():
    """Get the appropriate data store."""
    kv_store = get_vercel_kv_store()
    if kv_store:
        return VercelKVStore(kv_store)
    else:
        return search_store

class VercelKVStore(SearchDataStore):
    """Vercel KV-based data store for persistence."""
    
    def __init__(self, kv_client):
        super().__init__()
        self.kv = kv_client
    
    def add_search(self, search_data: Dict) -> bool:
        """Add search to Vercel KV."""
        try:
            # Add timestamp and ID
            if 'timestamp' not in search_data:
                search_data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Get existing searches
            existing = self.get_all_searches()
            search_data['id'] = len(existing) + 1
            existing.append(search_data)
            
            # Store back to KV
            self.kv.set(self.cache_key, json.dumps(existing))
            logging.info(f"Added search to Vercel KV for '{search_data.get('query', 'Unknown')}'")
            return True
        except Exception as e:
            logging.error(f"Error adding search to Vercel KV: {e}")
            return False
    
    def get_all_searches(self) -> List[Dict]:
        """Get all searches from Vercel KV."""
        try:
            data = self.kv.get(self.cache_key)
            if data:
                return json.loads(data)
            return []
        except Exception as e:
            logging.error(f"Error getting searches from Vercel KV: {e}")
            return []
    
    def get_recent_searches(self, limit: int = 10) -> List[Dict]:
        """Get recent searches from Vercel KV."""
        all_searches = self.get_all_searches()
        return all_searches[-limit:] if all_searches else []
    
    def get_stats(self) -> Dict:
        """Get stats from Vercel KV."""
        searches = self.get_all_searches()
        total = len(searches)
        cache_hits = len([s for s in searches if s.get('cache_status') == 'HIT'])
        cache_misses = len([s for s in searches if s.get('cache_status') == 'MISS'])
        
        return {
            'total_searches': total,
            'cache_hits': cache_hits,
            'cache_misses': cache_misses,
            'cache_hit_rate': (cache_hits / total * 100) if total > 0 else 0
        }
