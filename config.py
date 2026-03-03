#!/usr/bin/env python3
"""
Configuration Module - وحدة الإعدادات المركزية
Handles all path management and configuration for portable deployment
"""

import os
import json
from pathlib import Path

# Get the directory where this config file is located
PROJECT_ROOT = Path(__file__).parent.absolute()

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"
CONFIG_DIR = PROJECT_ROOT / "config"

# Data files
REGISTERED_NUMBERS_FILE = DATA_DIR / "registered_numbers.json"
LOG_FILE = LOGS_DIR / "djezzy.log"
CONFIG_FILE = CONFIG_DIR / "config.json"
ENV_FILE = PROJECT_ROOT / ".env"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
CONFIG_DIR.mkdir(exist_ok=True)

# Default configuration
DEFAULT_CONFIG = {
    "djezzy": {
        "max_attempts": 50,
        "timeout": 10,
        "retry_delay": 1,
    },
    "api": {
        "base_url": "https://apim.djezzy.dz",
        "registration_endpoint": "/mobile-api/oauth2/registration",
        "token_endpoint": "/mobile-api/oauth2/token",
        "invitation_endpoint": "/mobile-api/api/v1/services/mgm/send-invitation",
        "reward_endpoint": "/mobile-api/api/v1/services/mgm/activate-reward",
    },
    "logging": {
        "level": "INFO",
        "format": "%(asctime)s - %(levelname)s - %(message)s",
        "file": str(LOG_FILE),
    },
    "telegram": {
        "token": "",  # Will be set from .env
        "debug": False,
    }
}


def get_config():
    """Load configuration from file or return defaults"""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load config file: {e}")
    
    return DEFAULT_CONFIG


def save_config(config):
    """Save configuration to file"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error: Could not save config file: {e}")


def load_env():
    """Load environment variables from .env file"""
    env_vars = {}
    if ENV_FILE.exists():
        try:
            with open(ENV_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip()
        except Exception as e:
            print(f"Warning: Could not load .env file: {e}")
    
    return env_vars


def get_env(key, default=None):
    """Get environment variable"""
    import os
    return os.getenv(key, default)


def ensure_data_dirs():
    """Ensure all data directories exist"""
    DATA_DIR.mkdir(exist_ok=True, parents=True)
    LOGS_DIR.mkdir(exist_ok=True, parents=True)
    CONFIG_DIR.mkdir(exist_ok=True, parents=True)


# Print info
def print_paths():
    """Debug: Print all paths"""
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Data Directory: {DATA_DIR}")
    print(f"Logs Directory: {LOGS_DIR}")
    print(f"Config Directory: {CONFIG_DIR}")
    print(f"Registered Numbers File: {REGISTERED_NUMBERS_FILE}")
    print(f"Log File: {LOG_FILE}")


if __name__ == "__main__":
    ensure_data_dirs()
    print_paths()
