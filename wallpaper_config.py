#!/usr/bin/env python3
"""
User configuration file for Wallpaper Changer.

Modify the settings below to customize the application behavior.
After making changes, rebuild the application or restart it.
"""

# =============================================================================
# AUTO-CLOSE BEHAVIOR SETTINGS
# =============================================================================

# Set to True to automatically close the app after setting wallpaper
# Set to False to keep the app open for manual use
AUTO_CLOSE_AFTER_WALLPAPER = True

# Delay in milliseconds before auto-closing (only used if AUTO_CLOSE_AFTER_WALLPAPER is True)
AUTO_CLOSE_DELAY_MS = 1000  # 1 second

# =============================================================================
# WALLPAPER CATEGORIES
# =============================================================================

# You can modify or add to these categories
CUSTOM_GENRES = [
    "McLaren", "CyberTruck", "Tesla", "Sports Cars", "Ferrari", "Bugatti", 
    "Jeep Wrangler", "BMW", "Supra", "Porsche", "Audi", "Lamborghini", 
    "Koenigsegg", "Pagani latest", "Aston Martin", "Hennessey",
    # Add your custom categories here:
    # "Nature", "Landscapes", "Abstract", "Minimalist"
]

# =============================================================================
# API SETTINGS
# =============================================================================

# You can set your own Unsplash API key here
# Get one from: https://unsplash.com/developers
CUSTOM_API_KEY = ""  # Leave empty to use default

# =============================================================================
# DOWNLOAD SETTINGS
# =============================================================================

# Custom download directory (leave empty to use default)
CUSTOM_DOWNLOAD_DIR = ""  # Example: "C:/MyWallpapers"

# =============================================================================
# INSTRUCTIONS
# =============================================================================

def apply_config():
    """
    Apply the custom configuration to the main config.
    
    To use this configuration:
    1. Modify the settings above
    2. Run: python wallpaper_config.py
    3. Restart the application
    """
    import os
    import sys
    
    # Add current directory to path to import wallpaper_changer
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    try:
        # Import and modify the main config
        import wallpaper_changer.config as config
        
        # Apply auto-close settings
        config.AUTO_CLOSE_AFTER_WALLPAPER = AUTO_CLOSE_AFTER_WALLPAPER
        config.AUTO_CLOSE_DELAY_MS = AUTO_CLOSE_DELAY_MS
        
        # Apply custom genres if provided
        if CUSTOM_GENRES:
            config.GENRES = CUSTOM_GENRES
        
        # Apply custom API key if provided
        if CUSTOM_API_KEY:
            config.API_KEY = CUSTOM_API_KEY
            config.HEADERS["Authorization"] = f"Client-ID {CUSTOM_API_KEY}"
        
        # Apply custom download directory if provided
        if CUSTOM_DOWNLOAD_DIR:
            config.DOWNLOAD_DIR = os.path.expanduser(CUSTOM_DOWNLOAD_DIR)
            os.makedirs(config.DOWNLOAD_DIR, exist_ok=True)
        
        print("✅ Configuration applied successfully!")
        print(f"📁 Auto-close: {AUTO_CLOSE_AFTER_WALLPAPER}")
        print(f"⏱️  Delay: {AUTO_CLOSE_DELAY_MS}ms")
        print(f"🎯 Categories: {len(CUSTOM_GENRES)} genres")
        
        return True
        
    except ImportError as e:
        print(f"❌ Could not import wallpaper_changer: {e}")
        print("💡 Make sure you're running this from the project directory")
        return False
    except Exception as e:
        print(f"❌ Error applying configuration: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Wallpaper Changer Configuration")
    print("=" * 40)
    
    if apply_config():
        print("\n🎉 Configuration ready!")
        print("💡 You can now run the application with your custom settings.")
    else:
        print("\n❌ Configuration failed!")
        print("💡 Please check the error messages above.")
