"""
Configuration module for the Wallpaper Changer application.

Contains all constants, API keys, and configuration settings.
"""

import os
from typing import List
from pathlib import Path

# Unsplash API Configuration
API_KEY: str = os.environ.get("UNSPLASH_API_KEY", "APIKEY")
UNSPLASH_API_BASE_URL: str = "https://api.unsplash.com"

# API Headers
HEADERS = {
    "Authorization": f"Client-ID {API_KEY}",
    "Accept-Version": "v1"
}

# File and Directory Configuration
DOWNLOAD_DIR: str = os.path.expanduser("~/OneDrive/Pictures/Unsplash_Wallpapers")

# Ensure download directory exists
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Available wallpaper genres/categories
GENRES: List[str] = [
    # Supercars & Sports Cars
    "McLaren", "CyberTruck", "Tesla", "Sports Cars", "Ferrari", "Bugatti",
    "Jeep Wrangler", "BMW", "Supra", "Porsche", "Audi", "Lamborghini",
    "Koenigsegg", "Pagani Latest", "Aston Martin", "Hennessey",
    "Mustang", "Dodge Challenger", "Chevrolet Camaro", "Nissan GTR", "Corvette",
    
    # Luxury Cars & SUVs
    "Rolls Royce", "Bentley", "Mercedes Benz", "Range Rover", "Cadillac Escalade",
    "Genesis", "Lexus", "Maybach",

    # Hypercars & Concept
    "Lotus Evija", "Rimac Nevera", "Devel Sixteen", "Concept Cars", "Electric Supercars",

    # Aircrafts & Jets
    "Private Jets", "Fighter Jets", "Boeing 747", "Airbus A380", "Helicopters",
    "Military Aircraft", "Stealth Jets", "Vintage Planes",

    # Luxury Lifestyle
    "Yachts", "Luxury Villas", "Penthouse Interiors", "Exotic Locations", 
    "Luxury Watches", "Designer Fashion", "Millionaire Lifestyle",
    
    # Bonus Aesthetic
    "Night City Drives", "Garage Goals", "Jet + Car Combos", "Highway Rolls"
]


# API Request Configuration
DEFAULT_PER_PAGE: int = 20
DEFAULT_ORIENTATION: str = "landscape"
REQUEST_TIMEOUT: int = 10
DOWNLOAD_CHUNK_SIZE: int = 1024

# Application Configuration
APP_TITLE: str = "PixelDrive - Premium Automotive Wallpapers Made by Gurveer ❣️"
APP_GEOMETRY = (100, 100, 1000, 800)  # x, y, width, height

# Auto-close behavior configuration
AUTO_CLOSE_AFTER_WALLPAPER: bool = False  # Set to False to keep app open after setting wallpaper
AUTO_CLOSE_DELAY_MS: int = 1000  # Delay in milliseconds before auto-closing

# Application icon configuration
APP_ICON_PATH: str = os.path.join(os.path.dirname(__file__), "resources", "icon.ico")
APP_ICON_FALLBACK: str = ""  # Fallback icon path if main icon not found

# UI Configuration
PREVIEW_SIZE = (300, 200)
THUMBNAIL_SIZE = (150, 100)
BUTTON_MIN_HEIGHT: int = 35
LIST_MIN_HEIGHT: int = 200
HISTORY_MAX_HEIGHT: int = 150

# Logging Configuration
LOG_LEVEL: str = "INFO"
LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
