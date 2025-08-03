"""
Worker thread for fetching photos from Unsplash API.
"""

import logging
from typing import List, Dict, Any

from PyQt5.QtCore import QThread, pyqtSignal

from wallpaper_changer.api import UnsplashAPI

logger = logging.getLogger(__name__)


class FetchWorker(QThread):
    """Worker thread for fetching photos from Unsplash API."""
    
    # Signals
    photos = pyqtSignal(list)  # Emitted when photos are successfully fetched
    error = pyqtSignal(str)    # Emitted when an error occurs
    
    def __init__(self, query: str, parent=None):
        """
        Initialize the fetch worker.
        
        Args:
            query: Search query for photos
            parent: Parent QObject
        """
        super().__init__(parent)
        self.query = query
        self.api = UnsplashAPI()
    
    def run(self):
        """
        Run the worker thread to fetch photos.
        
        This method runs in a separate thread and emits signals
        to communicate with the main thread.
        """
        try:
            logger.info(f"Starting photo fetch for query: '{self.query}'")
            photos = self.api.search_photos(self.query)
            
            if photos:
                logger.info(f"Successfully fetched {len(photos)} photos")
                self.photos.emit(photos)
            else:
                logger.warning(f"No photos found for query: '{self.query}'")
                self.photos.emit([])
                
        except Exception as e:
            error_msg = f"Failed to fetch photos: {str(e)}"
            logger.error(error_msg)
            self.error.emit(error_msg)
            self.photos.emit([])  # Emit empty list as fallback
