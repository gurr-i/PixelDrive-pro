"""
Legacy compatibility layer for the original startupwallpaper.py script.

This file maintains backward compatibility while using the new modular structure.
For new installations, use: python -m wallpaper_changer.main
"""

import sys
import warnings

# Show deprecation warning
warnings.warn(
    "This script is deprecated. Please use 'python -m wallpaper_changer.main' instead.",
    DeprecationWarning,
    stacklevel=2
)

# Import from the new modular structure
try:
    from wallpaper_changer.main import main

    # For backward compatibility, also expose the main classes
    from wallpaper_changer.gui import WallpaperApp
    from wallpaper_changer.workers import FetchWorker, DownloadWorker
    from wallpaper_changer.config import *
    from wallpaper_changer.gui.styles import DarkTheme

    # Legacy variable for backward compatibility
    dark_theme = DarkTheme.get_stylesheet()

except ImportError as e:
    print(f"Error importing new modules: {e}")
    print("Please ensure the wallpaper_changer package is properly installed.")
    sys.exit(1)


if __name__ == "__main__":
    # Run the main application
    main()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WallpaperApp()
    window.show()
    sys.exit(app.exec_())