"""
Unsplash API client for fetching photos.
"""

import logging
import requests
from typing import List, Dict, Any, Optional
from requests.exceptions import RequestException, Timeout, ConnectionError

from wallpaper_changer.config import (
    UNSPLASH_API_BASE_URL, HEADERS, DEFAULT_PER_PAGE,
    DEFAULT_ORIENTATION, REQUEST_TIMEOUT
)

logger = logging.getLogger(__name__)


class UnsplashAPIError(Exception):
    """Custom exception for Unsplash API errors."""
    pass


class UnsplashAPI:
    """Client for interacting with the Unsplash API."""
    
    def __init__(self):
        """Initialize the Unsplash API client."""
        self.base_url = UNSPLASH_API_BASE_URL
        self.headers = HEADERS
        self.timeout = REQUEST_TIMEOUT
    
    def search_photos(
        self, 
        query: str, 
        per_page: int = DEFAULT_PER_PAGE,
        orientation: str = DEFAULT_ORIENTATION
    ) -> List[Dict[str, Any]]:
        """
        Search for photos on Unsplash.
        
        Args:
            query: Search query string
            per_page: Number of photos to return (max 30)
            orientation: Photo orientation ('landscape', 'portrait', 'squarish')
            
        Returns:
            List of photo dictionaries from Unsplash API
            
        Raises:
            requests.RequestException: If the API request fails
        """
        try:
            url = f"{self.base_url}/search/photos"
            params = {
                "query": query,
                "per_page": min(per_page, 30),  # Unsplash API limit
                "orientation": orientation
            }
            
            logger.info(f"Searching for photos with query: '{query}'")
            response = requests.get(
                url, 
                headers=self.headers, 
                params=params, 
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            photos = data.get("results", [])
            
            logger.info(f"Found {len(photos)} photos for query: '{query}'")
            return photos
            
        except Timeout as e:
            error_msg = f"Request timeout while searching for '{query}'"
            logger.error(error_msg)
            raise UnsplashAPIError(error_msg) from e
        except ConnectionError as e:
            error_msg = f"Connection error while searching for '{query}'"
            logger.error(error_msg)
            raise UnsplashAPIError(error_msg) from e
        except requests.HTTPError as e:
            if e.response.status_code == 403:
                error_msg = "API rate limit exceeded or invalid API key"
            elif e.response.status_code == 404:
                error_msg = "API endpoint not found"
            else:
                error_msg = f"HTTP error {e.response.status_code} while searching for '{query}'"
            logger.error(error_msg)
            raise UnsplashAPIError(error_msg) from e
        except RequestException as e:
            error_msg = f"Request failed while searching for '{query}': {str(e)}"
            logger.error(error_msg)
            raise UnsplashAPIError(error_msg) from e
    
    def get_photo_info(self, photo_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific photo.
        
        Args:
            photo_id: Unsplash photo ID
            
        Returns:
            Photo information dictionary or None if not found
            
        Raises:
            requests.RequestException: If the API request fails
        """
        try:
            url = f"{self.base_url}/photos/{photo_id}"
            
            logger.info(f"Fetching photo info for ID: {photo_id}")
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Failed to get photo info for ID '{photo_id}': {str(e)}")
            raise
    
    def download_photo(self, photo_url: str, file_path: str, progress_callback=None) -> bool:
        """
        Download a photo from Unsplash.
        
        Args:
            photo_url: URL of the photo to download
            file_path: Local path where to save the photo
            progress_callback: Optional callback function for progress updates
            
        Returns:
            True if download successful, False otherwise
        """
        try:
            logger.info(f"Downloading photo from: {photo_url}")
            response = requests.get(photo_url, stream=True, timeout=self.timeout)
            response.raise_for_status()
            
            total_size = int(response.headers.get("content-length", 0))
            downloaded = 0
            
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        downloaded += len(chunk)
                        file.write(chunk)
                        
                        if progress_callback and total_size > 0:
                            progress = int((downloaded / total_size) * 100)
                            progress_callback(progress)
            
            logger.info(f"Successfully downloaded photo to: {file_path}")
            return True
            
        except requests.RequestException as e:
            logger.error(f"Failed to download photo from '{photo_url}': {str(e)}")
            return False
        except IOError as e:
            logger.error(f"Failed to save photo to '{file_path}': {str(e)}")
            return False
    
    def get_photo_thumbnail(self, thumbnail_url: str) -> Optional[bytes]:
        """
        Get photo thumbnail data.
        
        Args:
            thumbnail_url: URL of the thumbnail image
            
        Returns:
            Thumbnail image data as bytes or None if failed
        """
        try:
            response = requests.get(thumbnail_url, timeout=5)
            response.raise_for_status()
            return response.content
            
        except requests.RequestException as e:
            logger.error(f"Failed to get thumbnail from '{thumbnail_url}': {str(e)}")
            return None
