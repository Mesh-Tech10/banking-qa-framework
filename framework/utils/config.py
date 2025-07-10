import yaml
import os

class ConfigManager:
    """Manages test configuration"""
    
    def __init__(self, config_file="config/test_config.yaml"):
        self.config_file = config_file
        self._config = None
    
    @property
    def config(self):
        """Load and return configuration"""
        if self._config is None:
            with open(self.config_file, 'r') as file:
                self._config = yaml.safe_load(file)
        return self._config
    
    def get(self, key, default=None):
        """Get configuration value by key"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
