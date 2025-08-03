"""
Main entry point for the Wallpaper Changer application.
"""

import sys
import logging
from PyQt5.QtWidgets import QApplication

from wallpaper_changer.config import LOG_LEVEL, LOG_FORMAT
from wallpaper_changer.gui import WallpaperApp


def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
        format=LOG_FORMAT
    )


def main():
    """Main entry point for the application."""
    # Set up logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Create QApplication
        app = QApplication(sys.argv)
        
        # Create and show main window
        window = WallpaperApp()
        window.show()
        
        # Start event loop
        sys.exit(app.exec_())
        
    except Exception as e:
        logger.error(f"Application failed to start: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
