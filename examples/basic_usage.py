#!/usr/bin/env python3
"""
Basic usage example for the Wallpaper Changer API.

This example demonstrates how to use the wallpaper changer components
programmatically without the GUI.
"""

import sys
import os
import logging

# Add the parent directory to the path so we can import wallpaper_changer
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wallpaper_changer.api import UnsplashAPI
from wallpaper_changer.utils import WallpaperManager
from wallpaper_changer.config import DOWNLOAD_DIR, GENRES

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def download_and_set_wallpaper(query: str = "Tesla"):
    """
    Download and set a wallpaper programmatically.
    
    Args:
        query: Search query for the wallpaper
    """
    try:
        # Initialize API client
        api = UnsplashAPI()
        wallpaper_manager = WallpaperManager()
        
        logger.info(f"Searching for photos with query: '{query}'")
        
        # Search for photos
        photos = api.search_photos(query, per_page=5)
        
        if not photos:
            logger.error("No photos found")
            return False
        
        # Select the first photo
        photo = photos[0]
        logger.info(f"Selected photo by: {photo.get('user', {}).get('name', 'Unknown')}")
        
        # Get the download URL
        image_url = photo.get("urls", {}).get("regular", "")
        if not image_url:
            logger.error("No image URL found")
            return False
        
        # Generate filename
        photo_id = photo.get('id', 'unsplash')
        filename = f"{photo_id}_example.jpg"
        file_path = os.path.join(DOWNLOAD_DIR, filename)
        
        logger.info(f"Downloading to: {file_path}")
        
        # Download the photo
        success = api.download_photo(image_url, file_path)
        
        if not success:
            logger.error("Failed to download photo")
            return False
        
        logger.info("Download completed successfully")
        
        # Set as wallpaper
        logger.info("Setting as desktop wallpaper...")
        success = wallpaper_manager.set_desktop_wallpaper(file_path)
        
        if success:
            logger.info("Wallpaper set successfully!")
            return True
        else:
            logger.error("Failed to set wallpaper")
            return False
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return False


def list_available_genres():
    """List all available wallpaper genres."""
    logger.info("Available wallpaper genres:")
    for i, genre in enumerate(GENRES, 1):
        print(f"{i:2d}. {genre}")


if __name__ == "__main__":
    print("Wallpaper Changer - Basic Usage Example")
    print("=" * 40)
    
    # List available genres
    list_available_genres()
    
    # Use command line argument or default
    query = sys.argv[1] if len(sys.argv) > 1 else "Tesla"
    
    print(f"\nDownloading and setting wallpaper for: '{query}'")
    print("-" * 40)
    
    success = download_and_set_wallpaper(query)
    
    if success:
        print("\n✅ Success! Wallpaper has been set.")
    else:
        print("\n❌ Failed to set wallpaper.")
        sys.exit(1)
