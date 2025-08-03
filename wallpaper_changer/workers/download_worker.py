"""
Worker thread for downloading photos from Unsplash.
"""

import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage

from wallpaper_changer.api import UnsplashAPI
from wallpaper_changer.config import DOWNLOAD_DIR

logger = logging.getLogger(__name__)


class DownloadWorker(QThread):
    """Worker thread for downloading photos from Unsplash."""
    
    # Signals
    progress = pyqtSignal(int)              # Emitted with download progress (0-100)
    finished = pyqtSignal(str, QPixmap)     # Emitted when download completes (path, thumbnail)
    error = pyqtSignal(str)                 # Emitted when an error occurs
    
    def __init__(self, photo: Dict[str, Any], parent=None):
        """
        Initialize the download worker.
        
        Args:
            photo: Photo dictionary from Unsplash API
            parent: Parent QObject
        """
        super().__init__(parent)
        self.photo = photo
        self.api = UnsplashAPI()
    
    def run(self):
        """
        Run the worker thread to download a photo.
        
        This method runs in a separate thread and emits signals
        to communicate with the main thread.
        """
        try:
            # Get image URL
            image_url = self.photo.get("urls", {}).get("full", "")
            if not image_url:
                self.error.emit("No image URL found in photo data")
                self.finished.emit("", QPixmap())
                return
            
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            photo_id = self.photo.get('id', 'unsplash')
            filename = f"{photo_id}_{timestamp}.jpg"
            image_path = os.path.join(DOWNLOAD_DIR, filename)
            
            logger.info(f"Starting download to: {image_path}")
            
            # Download the image with progress callback
            success = self.api.download_photo(
                image_url, 
                image_path, 
                progress_callback=self.progress.emit
            )
            
            if not success:
                self.error.emit("Failed to download image")
                self.finished.emit("", QPixmap())
                return
            
            # Get thumbnail for preview
            thumbnail_pixmap = self._get_thumbnail_pixmap()
            
            logger.info(f"Download completed successfully: {image_path}")
            self.finished.emit(image_path, thumbnail_pixmap)
            
        except Exception as e:
            error_msg = f"Download failed: {str(e)}"
            logger.error(error_msg)
            self.error.emit(error_msg)
            self.finished.emit("", QPixmap())
    
    def _get_thumbnail_pixmap(self) -> QPixmap:
        """
        Get thumbnail pixmap for the downloaded photo.
        
        Returns:
            QPixmap object for thumbnail or empty pixmap if failed
        """
        try:
            thumbnail_url = self.photo.get("urls", {}).get("thumb", "")
            if not thumbnail_url:
                return QPixmap()
            
            thumbnail_data = self.api.get_photo_thumbnail(thumbnail_url)
            if thumbnail_data:
                return QPixmap.fromImage(QImage.fromData(thumbnail_data))
            
        except Exception as e:
            logger.warning(f"Failed to get thumbnail: {str(e)}")
        
        return QPixmap()
