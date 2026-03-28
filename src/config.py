import json
import os

DEFAULT_CONTINENTS = {
    "asia": {
        "Hong Kong": "HKD", "China": "CNY", "Indonesia": "IDR", "India": "INR", 
        "Japan": "JPY", "South Korea": "KRW", "Malaysia": "MYR", 
        "Philippines": "PHP", "Singapore": "SGD", "Thailand": "THB",
        "Israel": "ILS"
    },
    "europe": {
        "Switzerland": "CHF", "Czech Republic": "CZK", "Denmark": "DKK", 
        "United Kingdom": "GBP", "Hungary": "HUF", "Iceland": "ISK", 
        "Norway": "NOK", "Poland": "PLN", "Romania": "RON", 
        "Sweden": "SEK", "Turkey": "TRY"
    },
    "america": {
        "Canada": "CAD", "Mexico": "MXN", "United States": "USD", "Brazil": "BRL"
    },
    "oceania_africa": {
        "Australia": "AUD", "New Zealand": "NZD", "South Africa": "ZAR"
    }
}

class Config:
    def __init__(self, config_path = "../config.json"):
        self.config_path = config_path
        self.continents = self._load_config()

    def _load_config(self):
        if not os.path.exists(self.config_path):
            return DEFAULT_CONTINENTS
        
        try:
            with open(self.config_path, "r") as f:
                data = json.load(f)
                return data.get("continents", DEFAULT_CONTINENTS)
        except (json.JSONDecodeError, IOError):
            return DEFAULT_CONTINENTS

    def get_continents(self):
        return self.continents

