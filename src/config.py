import yaml
from pathlib import Path
from typing import Any, Dict

class Config:
    """Loads and manages application configuration from config.yml"""
    
    _instance = None
    _config: Dict[str, Any] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        """Load configuration from config.yml if it exists"""
        config_path = Path("/etc/goblin-speaks/config.yml")
        
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    self._config = yaml.safe_load(f) or {}
                print(f"Configuration loaded from {config_path}")
            except Exception as e:
                print(f"Error loading config file: {e}. Using defaults.")
                self._config = {}
        else:
            print("No config file found. Using default values.")
            self._config = {}
        
        print("")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value with optional default"""
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    @staticmethod
    def reload():
        """Reload configuration from file"""
        Config._instance = None
        return Config()