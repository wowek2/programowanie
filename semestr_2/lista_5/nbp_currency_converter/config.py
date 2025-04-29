"""
Configuration management for the NBP Currency Converter application.
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import json

from utils.errors import ConfigurationError


# Default configuration values
DEFAULT_CONFIG = {
    "app": {
        "title": "NBP Currency Converter",
        "theme": "BOOTSTRAP",
        "debug": False,
        "host": "0.0.0.0",
        "port": 8050
    },
    "data": {
        "request_timeout": 10  # Request timeout in seconds
    },
    "ui": {
        "default_amount": 1,
        "default_from_currency": "USD",
        "default_to_currency": "PLN",
        "default_period": 90,  # 3 months
        "chart_height": 400,
        "animate_charts": True
    },
    "logging": {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "file": None  # No file logging by default
    }
}


class Config:
    """Configuration manager for the application.
    
    This class handles loading configuration
    and provides access to configuration values.
    
    Attributes:
        config (Dict[str, Any]): The current configuration
    """
    
    def __init__(self):
        """Initialize the configuration manager.
        
        Args:
            config_path: Path to a JSON configuration file (optional)
        """
        self.config = DEFAULT_CONFIG.copy()
            
        # Set up logging based on configuration
        self._setup_logging()

    
    def _setup_logging(self) -> None:
        """Set up logging."""
        log_config = self.config["logging"]
        
        # Set up basic logging
        logging.basicConfig(
            level=getattr(logging, log_config["level"]),
            format=log_config["format"]
        )
    
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """Get a configuration value.
        
        Args:
            section: Configuration section
            key: Configuration key
            default: Default value if key is not found
            
        Returns:
            The configuration value or default
        """
        if section in self.config and key in self.config[section]:
            return self.config[section][key]
        return default


# Global configuration instance
config = Config()