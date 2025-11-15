from typing import Dict, List, Any
from datetime import datetime, timedelta


class SessionStorage:
    """In-memory storage for search results and sessions."""

    def __init__(self):
        self._searches: Dict[str, Dict[str, Any]] = {}

    def store_search(self, search_id: str, search_request: Dict, results: List[Dict]):
        """Store search results."""
        self._searches[search_id] = {
            "search_id": search_id,
            "request": search_request,
            "results": results,
            "created_at": datetime.utcnow()
        }

    def get_search(self, search_id: str) -> Dict[str, Any]:
        """Get search results by ID."""
        return self._searches.get(search_id)

    def get_all_searches(self) -> List[Dict[str, Any]]:
        """Get all stored searches."""
        return list(self._searches.values())

    def delete_search(self, search_id: str):
        """Delete a search."""
        if search_id in self._searches:
            del self._searches[search_id]

    def cleanup_old_searches(self, hours: int = 24):
        """Delete searches older than specified hours."""
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        searches_to_delete = []

        for search_id, search_data in self._searches.items():
            if search_data.get("created_at") < cutoff:
                searches_to_delete.append(search_id)

        for search_id in searches_to_delete:
            del self._searches[search_id]

    def clear_all(self):
        """Clear all searches."""
        self._searches.clear()


# Global session storage instance
session_storage = SessionStorage()
