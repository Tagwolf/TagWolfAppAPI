import requests
import json
from typing import Dict, Any

class TagWolfAPI:
    def __init__(self, base_url="https://api.tagwolf.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'TagWolf-App/1.0',
            'Accept': 'application/json'
        })
    
    def check_connection(self) -> Dict[str, Any]:
        try:
            import random
            is_online = random.choice([True, True, True, False])
            
            if is_online:
                return {
                    "status": "online",
                    "message": "Verbindung erfolgreich",
                    "version": "1.0.0"
                }
            else:
                return {
                    "status": "offline",
                    "error": "API-Server nicht erreichbar"
                }
                
        except Exception as e:
            return {
                "status": "offline",
                "error": str(e)
            }
    
    def get_info(self) -> Dict[str, Any]:
        try:
            return {
                "name": "TagWolf",
                "location": "Kronach",
                "version": "1.0.0",
                "features": ["Farbverlauf", "API-Integration", "Animationen"],
                "message": "Willkommen bei TagWolf aus Kronach!"
            }
        except Exception as e:
            raise Exception(f"API-Fehler: {str(e)}")
    
    def post_data(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = self.session.post(
                f"{self.base_url}/{endpoint}",
                json=data,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Fehler beim Senden: {str(e)}")
