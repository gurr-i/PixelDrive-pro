"""
Cross-platform wallpaper management utilities.
"""

import os
import sys
import ctypes
import subprocess
import logging
from typing import Optional

try:
    import winreg
except ImportError:
    winreg = None  # Not available on non-Windows platforms

logger = logging.getLogger(__name__)


class WallpaperManager:
    """Cross-platform wallpaper management."""
    
    @staticmethod
    def set_desktop_wallpaper(image_path: str) -> bool:
        """
        Set desktop wallpaper across different platforms.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            True if successful, False otherwise
        """
        if not os.path.exists(image_path):
            logger.error(f"Image file does not exist: {image_path}")
            return False
        
        try:
            if sys.platform == "win32":
                return WallpaperManager._set_windows_desktop(image_path)
            elif sys.platform == "darwin":
                return WallpaperManager._set_macos_desktop(image_path)
            elif sys.platform.startswith("linux"):
                return WallpaperManager._set_linux_desktop(image_path)
            else:
                logger.error(f"Unsupported platform: {sys.platform}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to set desktop wallpaper: {str(e)}")
            return False
    
    @staticmethod
    def set_lockscreen_wallpaper(image_path: str) -> bool:
        """
        Set lockscreen wallpaper across different platforms.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            True if successful, False otherwise
        """
        if not os.path.exists(image_path):
            logger.error(f"Image file does not exist: {image_path}")
            return False
        
        try:
            if sys.platform == "win32":
                return WallpaperManager._set_windows_lockscreen(image_path)
            elif sys.platform == "darwin":
                # macOS doesn't have separate lockscreen wallpaper
                logger.info("macOS uses desktop wallpaper for lockscreen")
                return WallpaperManager._set_macos_desktop(image_path)
            elif sys.platform.startswith("linux"):
                return WallpaperManager._set_linux_lockscreen(image_path)
            else:
                logger.error(f"Unsupported platform: {sys.platform}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to set lockscreen wallpaper: {str(e)}")
            return False
    
    @staticmethod
    def _set_windows_desktop(image_path: str) -> bool:
        """Set Windows desktop wallpaper."""
        try:
            # Convert to absolute path with Windows path separators
            abs_path = os.path.abspath(image_path).replace('/', '\\')
            result = ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 3)
            
            if result:
                logger.info(f"Successfully set Windows desktop wallpaper: {abs_path}")
                return True
            else:
                logger.error("Failed to set Windows desktop wallpaper")
                return False
                
        except Exception as e:
            logger.error(f"Windows desktop wallpaper error: {str(e)}")
            return False
    
    @staticmethod
    def _set_windows_lockscreen(image_path: str) -> bool:
        """Set Windows lockscreen wallpaper."""
        if not winreg:
            logger.error("winreg module not available")
            return False
        
        try:
            abs_path = os.path.abspath(image_path).replace('/', '\\')
            reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\PersonalizationCSP"
            
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_ALL_ACCESS)
            except FileNotFoundError:
                key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
            
            winreg.SetValueEx(key, "LockScreenImagePath", 0, winreg.REG_SZ, abs_path)
            winreg.SetValueEx(key, "LockScreenImageStatus", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            
            # Also set as desktop wallpaper as fallback
            ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 3)
            
            logger.info(f"Successfully set Windows lockscreen wallpaper: {abs_path}")
            return True
            
        except PermissionError:
            logger.error("Permission denied: Run as administrator to set lockscreen")
            return False
        except Exception as e:
            logger.error(f"Windows lockscreen wallpaper error: {str(e)}")
            return False
    
    @staticmethod
    def _set_macos_desktop(image_path: str) -> bool:
        """Set macOS desktop wallpaper."""
        try:
            abs_path = os.path.abspath(image_path)
            cmd = [
                "osascript", "-e",
                f'tell app "System Events" to set picture of every desktop to "{abs_path}"'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Successfully set macOS desktop wallpaper: {abs_path}")
                return True
            else:
                logger.error(f"macOS wallpaper command failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"macOS desktop wallpaper error: {str(e)}")
            return False
    
    @staticmethod
    def _set_linux_desktop(image_path: str) -> bool:
        """Set Linux desktop wallpaper (GNOME)."""
        try:
            abs_path = os.path.abspath(image_path)
            cmd = [
                "gsettings", "set", "org.gnome.desktop.background",
                "picture-uri", f"file://{abs_path}"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Successfully set Linux desktop wallpaper: {abs_path}")
                return True
            else:
                logger.error(f"Linux wallpaper command failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Linux desktop wallpaper error: {str(e)}")
            return False
    
    @staticmethod
    def _set_linux_lockscreen(image_path: str) -> bool:
        """Set Linux lockscreen wallpaper (GNOME)."""
        try:
            abs_path = os.path.abspath(image_path)
            cmd = [
                "gsettings", "set", "org.gnome.desktop.screensaver",
                "picture-uri", f"file://{abs_path}"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Successfully set Linux lockscreen wallpaper: {abs_path}")
                return True
            else:
                logger.error(f"Linux lockscreen command failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Linux lockscreen wallpaper error: {str(e)}")
            return False
