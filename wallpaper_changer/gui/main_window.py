"""
Main window GUI for the wallpaper changer application.
"""

import os
import random
import logging
from typing import List, Dict, Any, Optional

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton,
    QProgressBar, QLabel, QComboBox, QListWidget, QListWidgetItem,
    QApplication, QFrame, QHBoxLayout
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage, QIcon, QFont

from wallpaper_changer.config import (
    GENRES, APP_TITLE, APP_GEOMETRY,
    AUTO_CLOSE_AFTER_WALLPAPER, AUTO_CLOSE_DELAY_MS, APP_ICON_PATH
)
from wallpaper_changer.workers import FetchWorker, DownloadWorker
from wallpaper_changer.utils import WallpaperManager
from wallpaper_changer.gui.styles import DarkTheme
from wallpaper_changer.gui.widgets import ImagePreviewCard, EnhancedListWidget, LoadingSpinner

logger = logging.getLogger(__name__)


class WallpaperApp(QMainWindow):
    """Main application window for the wallpaper changer."""
    
    def __init__(self):
        """Initialize the main application window."""
        super().__init__()
        
        # Application state
        self.downloaded_paths: List[str] = []
        self.photos: List[Dict[str, Any]] = []
        self.selected_photo: Optional[Dict[str, Any]] = None
        self.wallpaper_manager = WallpaperManager()
        
        # Worker threads
        self.fetch_worker: Optional[FetchWorker] = None
        self.download_worker: Optional[DownloadWorker] = None
        
        # Initialize UI
        self._setup_window()
        self._init_ui()
        self._apply_theme()
        
        # Start auto-wallpaper change on startup
        self.auto_change_wallpaper()
    
    def _setup_window(self):
        """Set up the main window properties."""
        self.setWindowTitle(APP_TITLE)
        self.setGeometry(*APP_GEOMETRY)

        # Set application icon
        if os.path.exists(APP_ICON_PATH):
            icon = QIcon(APP_ICON_PATH)
            self.setWindowIcon(icon)
            # Also set as application icon
            QApplication.instance().setWindowIcon(icon)
        else:
            logger.warning(f"Icon file not found: {APP_ICON_PATH}")
    
    def _init_ui(self):
        """Initialize the user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout with better spacing
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Create main sections
        self._create_header_section(layout)
        self._create_search_section(layout)
        self._create_content_section(layout)
        self._create_status_section(layout)

        layout.addStretch()
        central_widget.setLayout(layout)
    
    def _create_header_section(self, layout: QVBoxLayout):
        """Create the header section with title and subtitle."""
        header_frame = QFrame()
        header_frame.setProperty("class", "card")
        header_layout = QVBoxLayout()
        header_layout.setSpacing(8)

        # Title
        title_label = QLabel("🚗 PixelDrive")
        title_label.setProperty("class", "title")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont("Segoe UI", 24, QFont.Bold)
        title_label.setFont(title_font)

        # Subtitle
        subtitle_label = QLabel("Transform your desktop with stunning automotive photography")
        subtitle_label.setProperty("class", "subtitle")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setWordWrap(True)

        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        header_frame.setLayout(header_layout)

        layout.addWidget(header_frame)

    def _create_search_section(self, layout: QVBoxLayout):
        """Create the search section of the UI."""
        search_frame = QFrame()
        search_frame.setProperty("class", "card")
        search_layout = QHBoxLayout()
        search_layout.setSpacing(12)

        # Search input
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("🔍 Enter custom search query...")
        self.query_input.setMinimumHeight(45)

        # Genre selection
        self.genre_combo = QComboBox()
        self.genre_combo.addItems(["🎲 Random"] + [f"🏎️ {genre}" for genre in GENRES])
        self.genre_combo.setMinimumHeight(45)
        self.genre_combo.setMinimumWidth(200)

        # Fetch button with loading state
        self.fetch_button = QPushButton("✨ Fetch Photos")
        self.fetch_button.setMinimumHeight(45)
        self.fetch_button.setMinimumWidth(120)
        self.fetch_button.clicked.connect(self.fetch_photos)

        search_layout.addWidget(self.query_input, 2)
        search_layout.addWidget(self.genre_combo, 1)
        search_layout.addWidget(self.fetch_button, 0)

        search_frame.setLayout(search_layout)
        layout.addWidget(search_frame)
    
    def _create_content_section(self, layout: QVBoxLayout):
        """Create the main content section with photos and previews."""
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # Left side - Photo list
        left_frame = QFrame()
        left_frame.setProperty("class", "card")
        left_layout = QVBoxLayout()
        left_layout.setSpacing(12)

        # Photos list header
        photos_header = QLabel("📸 Available Photos")
        photos_header.setProperty("class", "title")
        photos_header.setFont(QFont("Segoe UI", 16, QFont.Bold))

        # Enhanced photo list
        self.preview_list = EnhancedListWidget()
        self.preview_list.setMinimumHeight(300)
        self.preview_list.setMinimumWidth(400)
        self.preview_list.itemClicked.connect(self.preview_selected)

        # Loading spinner for photo list
        self.photos_loading = LoadingSpinner(24)
        self.photos_loading.hide()

        left_layout.addWidget(photos_header)
        left_layout.addWidget(self.photos_loading, 0, Qt.AlignCenter)
        left_layout.addWidget(self.preview_list)
        left_frame.setLayout(left_layout)

        # Right side - Preview cards
        right_layout = QVBoxLayout()
        right_layout.setSpacing(16)

        # Selected preview card
        self.selected_preview = ImagePreviewCard(320, 240)

        # Downloaded preview card
        self.downloaded_preview = ImagePreviewCard(320, 180)

        right_layout.addWidget(self.selected_preview)
        right_layout.addWidget(self.downloaded_preview)
        right_layout.addStretch()

        content_layout.addWidget(left_frame, 2)
        content_layout.addLayout(right_layout, 1)

        layout.addLayout(content_layout)
    
    def _create_status_section(self, layout: QVBoxLayout):
        """Create the status and controls section."""
        # Progress and status frame
        status_frame = QFrame()
        status_frame.setProperty("class", "card")
        status_layout = QVBoxLayout()
        status_layout.setSpacing(12)

        # Progress bar with enhanced styling
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumHeight(20)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("Ready")

        # Status label with icon
        self.status_label = QLabel("🎯 Ready to fetch wallpapers")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Segoe UI", 12))

        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)

        # Download button
        self.download_button = QPushButton("💾 Download")
        self.download_button.setMinimumHeight(50)
        self.download_button.setMinimumWidth(120)
        self.download_button.clicked.connect(self.download_selected)
        self.download_button.setEnabled(False)

        # Set wallpaper buttons
        self.set_wallpaper_button = QPushButton("🖥️ Set Desktop")
        self.set_wallpaper_button.setMinimumHeight(50)
        self.set_wallpaper_button.setMinimumWidth(120)
        self.set_wallpaper_button.clicked.connect(self.set_wallpaper)
        self.set_wallpaper_button.setEnabled(False)

        self.set_lockscreen_button = QPushButton("🔒 Set Lockscreen")
        self.set_lockscreen_button.setMinimumHeight(50)
        self.set_lockscreen_button.setMinimumWidth(120)
        self.set_lockscreen_button.clicked.connect(self.set_lockscreen)
        self.set_lockscreen_button.setEnabled(False)

        button_layout.addWidget(self.download_button)
        button_layout.addWidget(self.set_wallpaper_button)
        button_layout.addWidget(self.set_lockscreen_button)
        button_layout.addStretch()

        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.progress_bar)
        status_layout.addLayout(button_layout)

        status_frame.setLayout(status_layout)
        layout.addWidget(status_frame)

        # History section (collapsible)
        self._create_history_section(layout)

    def _create_history_section(self, layout: QVBoxLayout):
        """Create the download history section."""
        history_frame = QFrame()
        history_frame.setProperty("class", "card")
        history_layout = QVBoxLayout()
        history_layout.setSpacing(8)

        # History header
        history_header = QLabel("📁 Download History")
        history_header.setProperty("class", "title")
        history_header.setFont(QFont("Segoe UI", 14, QFont.Bold))

        # History list
        self.history_list = QListWidget()
        self.history_list.setMaximumHeight(120)
        self.history_list.itemDoubleClicked.connect(self.set_wallpaper_from_history)

        history_layout.addWidget(history_header)
        history_layout.addWidget(self.history_list)
        history_frame.setLayout(history_layout)

        layout.addWidget(history_frame)
    
    def _apply_theme(self):
        """Apply the dark theme to the application."""
        self.setStyleSheet(DarkTheme.get_stylesheet())

    def auto_change_wallpaper(self):
        """Automatically fetch, download, and set a random wallpaper on startup."""
        query = random.choice(GENRES)
        self.status_label.setText(f"Fetching random {query} wallpaper...")

        self.fetch_worker = FetchWorker(query)
        self.fetch_worker.photos.connect(self.auto_download_random)
        self.fetch_worker.error.connect(self.show_error_and_close)
        self.fetch_worker.start()

    def auto_download_random(self, photos: List[Dict[str, Any]]):
        """Download a random photo from the fetched results."""
        if not photos:
            self.status_label.setText("No photos found")
            if AUTO_CLOSE_AFTER_WALLPAPER:
                QTimer.singleShot(AUTO_CLOSE_DELAY_MS, self.close)
            return

        self.photos = photos
        random_photo = random.choice(photos)

        self.download_worker = DownloadWorker(random_photo)
        self.download_worker.finished.connect(self.auto_set_wallpaper)
        self.download_worker.error.connect(self.show_error_and_close)
        self.download_worker.start()

        self.status_label.setText("Downloading random wallpaper...")

    def auto_set_wallpaper(self, path: str, pixmap: QPixmap):
        """Set the downloaded wallpaper and optionally close the app."""
        if path:
            self.downloaded_paths.append(path)
            success = self.wallpaper_manager.set_desktop_wallpaper(path)
            if success:
                self.status_label.setText("Wallpaper set successfully")
            else:
                self.status_label.setText("Failed to set wallpaper")

            # Only auto-close if configured to do so
            if AUTO_CLOSE_AFTER_WALLPAPER:
                QTimer.singleShot(AUTO_CLOSE_DELAY_MS, self.close)
            else:
                self.status_label.setText("Wallpaper set successfully - App ready for manual use")
        else:
            self.status_label.setText("Failed to download wallpaper")
            if AUTO_CLOSE_AFTER_WALLPAPER:
                QTimer.singleShot(AUTO_CLOSE_DELAY_MS, self.close)

    def fetch_photos(self):
        """Fetch photos based on user input."""
        # Clean up query
        query = self.query_input.text().strip() or self.genre_combo.currentText()
        # Remove emoji prefixes
        query = query.replace("🎲 ", "").replace("🏎️ ", "")
        if query == "Random":
            query = random.choice(GENRES)

        # Show loading state
        self.preview_list.clear()
        self.photos_loading.show()
        self.photos_loading.start_animation()
        self.selected_preview.show_placeholder()

        # Update UI state
        self.status_label.setText(f"🔍 Fetching {query} photos...")
        self.progress_bar.setFormat("Searching...")
        self.fetch_button.setEnabled(False)
        self.fetch_button.setText("⏳ Fetching...")

        # Disable action buttons
        self.download_button.setEnabled(False)
        self.set_wallpaper_button.setEnabled(False)
        self.set_lockscreen_button.setEnabled(False)

        self.fetch_worker = FetchWorker(query)
        self.fetch_worker.photos.connect(self.display_photos)
        self.fetch_worker.error.connect(self.show_error)
        self.fetch_worker.start()

    def display_photos(self, photos: List[Dict[str, Any]]):
        """Display fetched photos in the enhanced preview list."""
        self.photos = photos

        # Hide loading spinner
        self.photos_loading.hide()
        self.photos_loading.stop_animation()

        # Reset UI state
        self.fetch_button.setEnabled(True)
        self.fetch_button.setText("✨ Fetch Photos")

        if not photos:
            self.status_label.setText("❌ No photos found. Try a different search term.")
            self.progress_bar.setFormat("No results")
            return

        # Add photos to enhanced list with async thumbnail loading
        for i, photo in enumerate(photos):
            # Add item without thumbnail first for immediate feedback
            self.preview_list.add_photo_item(photo)

            # Load thumbnail asynchronously
            QTimer.singleShot(i * 100, lambda p=photo: self._load_thumbnail_async(p))

        # Update status
        self.status_label.setText(f"✅ Loaded {len(photos)} photos")
        self.progress_bar.setFormat(f"{len(photos)} photos loaded")

    def _load_thumbnail_async(self, photo: Dict[str, Any]):
        """Load thumbnail asynchronously to avoid blocking UI."""
        thumbnail_url = photo.get("urls", {}).get("thumb", "")
        if thumbnail_url:
            try:
                import requests
                response = requests.get(thumbnail_url, timeout=3)
                if response.status_code == 200:
                    pixmap = QPixmap.fromImage(QImage.fromData(response.content))
                    # Find the corresponding item and update it
                    for i in range(self.preview_list.count()):
                        item = self.preview_list.item(i)
                        if item and item.data(Qt.UserRole) == photo:
                            # Update the thumbnail in the custom widget
                            widget = self.preview_list.itemWidget(item)
                            if widget:
                                thumbnail_label = widget.findChild(QLabel)
                                if thumbnail_label:
                                    scaled_thumb = pixmap.scaled(
                                        64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation
                                    )
                                    thumbnail_label.setPixmap(scaled_thumb)
                            break
            except Exception as e:
                logger.warning(f"Failed to load thumbnail: {str(e)}")

    def preview_selected(self, item: QListWidgetItem):
        """Handle photo selection for enhanced preview."""
        try:
            photo = item.data(Qt.UserRole)
            self.selected_photo = photo

            # Enable download button
            self.download_button.setEnabled(True)

            # Show loading state in preview card
            author_name = photo.get('user', {}).get('name', 'Unknown')
            self.selected_preview.show_loading(f"Loading preview by {author_name}...")

            # Load preview image asynchronously
            QTimer.singleShot(50, lambda: self._load_preview_async(photo))

        except Exception as e:
            logger.error(f"Preview error: {str(e)}")
            self.selected_preview.show_error(f"Preview failed: {str(e)}")

    def _load_preview_async(self, photo: Dict[str, Any]):
        """Load preview image asynchronously."""
        try:
            image_url = photo.get("urls", {}).get("small", "")
            if image_url:
                import requests
                response = requests.get(image_url, timeout=5)
                if response.status_code == 200:
                    pixmap = QPixmap.fromImage(QImage.fromData(response.content))

                    # Create info text
                    author_name = photo.get('user', {}).get('name', 'Unknown')
                    width = photo.get('width', 0)
                    height = photo.get('height', 0)
                    info_text = f"📸 {author_name}"
                    if width and height:
                        info_text += f"\n📐 {width} × {height}"

                    self.selected_preview.show_image(pixmap, info_text)
                else:
                    self.selected_preview.show_error("Failed to load preview")
            else:
                self.selected_preview.show_error("No preview URL available")

        except Exception as e:
            logger.error(f"Async preview error: {str(e)}")
            self.selected_preview.show_error(f"Preview error: {str(e)}")

    def download_selected(self):
        """Download the selected photo with enhanced UI feedback."""
        if not self.selected_photo:
            self.status_label.setText("❌ Please select a photo first")
            return

        # Update UI state
        self.download_button.setEnabled(False)
        self.download_button.setText("⏳ Downloading...")
        self.status_label.setText("💾 Downloading high-resolution image...")
        self.progress_bar.setFormat("Downloading... %p%")

        # Show loading in downloaded preview
        author_name = self.selected_photo.get('user', {}).get('name', 'Unknown')
        self.downloaded_preview.show_loading(f"Downloading {author_name}'s photo...")

        self.download_worker = DownloadWorker(self.selected_photo)
        self.download_worker.progress.connect(self._update_download_progress)
        self.download_worker.finished.connect(self.on_download_finished)
        self.download_worker.error.connect(self.show_error)
        self.download_worker.start()

    def _update_download_progress(self, progress: int):
        """Update download progress with enhanced feedback."""
        self.progress_bar.setValue(progress)
        if progress < 100:
            self.progress_bar.setFormat(f"Downloading... {progress}%")
        else:
            self.progress_bar.setFormat("Processing...")

    def on_download_finished(self, path: str, pixmap: QPixmap):
        """Handle download completion with enhanced UI feedback."""
        # Reset download button
        self.download_button.setEnabled(True)
        self.download_button.setText("💾 Download")

        if path:
            self.downloaded_paths.append(path)

            # Add to history with enhanced styling
            filename = os.path.basename(path)
            item = QListWidgetItem(f"📁 {filename}")
            item.setData(Qt.UserRole, path)
            if not pixmap.isNull():
                item.setIcon(QIcon(pixmap))
            self.history_list.addItem(item)

            # Update downloaded preview card
            if not pixmap.isNull():
                author_name = self.selected_photo.get('user', {}).get('name', 'Unknown') if self.selected_photo else 'Unknown'
                info_text = f"✅ Downloaded\n📸 {author_name}\n📁 {filename}"
                self.downloaded_preview.show_image(pixmap, info_text)
            else:
                self.downloaded_preview.show_error("Downloaded but no preview available")

            # Enable wallpaper buttons
            self.set_wallpaper_button.setEnabled(True)
            self.set_lockscreen_button.setEnabled(True)

            # Success feedback
            self.status_label.setText("✅ Download completed successfully!")
            self.progress_bar.setFormat("Download complete")

            # Add success animation
            QTimer.singleShot(2000, lambda: self.progress_bar.setFormat("Ready"))
        else:
            self.downloaded_preview.show_error("Download failed")
            self.status_label.setText("❌ Download failed")
            self.progress_bar.setFormat("Download failed")

        # Reset progress bar after delay
        QTimer.singleShot(3000, lambda: self.progress_bar.setValue(0))

    def set_wallpaper(self, path: Optional[str] = None):
        """Set desktop wallpaper with enhanced feedback."""
        if not path and self.downloaded_paths:
            path = self.downloaded_paths[-1]

        if not path or not os.path.exists(path):
            self.status_label.setText("❌ No valid image selected")
            return

        # Show setting wallpaper feedback
        self.status_label.setText("🖥️ Setting desktop wallpaper...")
        self.progress_bar.setFormat("Setting wallpaper...")

        # Disable button temporarily
        self.set_wallpaper_button.setEnabled(False)
        self.set_wallpaper_button.setText("⏳ Setting...")

        # Use timer to allow UI update before blocking operation
        QTimer.singleShot(100, lambda: self._set_wallpaper_async(path, "desktop"))

    def set_lockscreen(self, path: Optional[str] = None):
        """Set lockscreen wallpaper with enhanced feedback."""
        if not path and self.downloaded_paths:
            path = self.downloaded_paths[-1]

        if not path or not os.path.exists(path):
            self.status_label.setText("❌ No valid image selected")
            return

        # Show setting wallpaper feedback
        self.status_label.setText("🔒 Setting lockscreen wallpaper...")
        self.progress_bar.setFormat("Setting lockscreen...")

        # Disable button temporarily
        self.set_lockscreen_button.setEnabled(False)
        self.set_lockscreen_button.setText("⏳ Setting...")

        # Use timer to allow UI update before blocking operation
        QTimer.singleShot(100, lambda: self._set_wallpaper_async(path, "lockscreen"))

    def _set_wallpaper_async(self, path: str, wallpaper_type: str):
        """Set wallpaper asynchronously with proper feedback."""
        try:
            if wallpaper_type == "desktop":
                success = self.wallpaper_manager.set_desktop_wallpaper(path)
                button = self.set_wallpaper_button
                success_msg = "✅ Desktop wallpaper set successfully!"
                fail_msg = "❌ Failed to set desktop wallpaper"
                button_text = "🖥️ Set Desktop"
            else:
                success = self.wallpaper_manager.set_lockscreen_wallpaper(path)
                button = self.set_lockscreen_button
                success_msg = "✅ Lockscreen wallpaper set successfully!"
                fail_msg = "❌ Failed to set lockscreen wallpaper"
                button_text = "🔒 Set Lockscreen"

            # Update UI based on result
            if success:
                self.status_label.setText(success_msg)
                self.progress_bar.setFormat("Wallpaper set!")
            else:
                self.status_label.setText(fail_msg)
                self.progress_bar.setFormat("Failed to set wallpaper")

            # Re-enable button
            button.setEnabled(True)
            button.setText(button_text)

            # Reset progress bar after delay
            QTimer.singleShot(3000, lambda: self.progress_bar.setFormat("Ready"))

        except Exception as e:
            logger.error(f"Error setting {wallpaper_type} wallpaper: {str(e)}")
            self.status_label.setText(f"❌ Error setting {wallpaper_type} wallpaper")
            button.setEnabled(True)
            button.setText(button_text)

    def set_wallpaper_from_history(self, item: QListWidgetItem):
        """Set wallpaper from history item."""
        path = item.data(Qt.UserRole)
        if path and os.path.exists(path):
            self.set_wallpaper(path)

    def show_error(self, message: str):
        """Show error message and reset UI state."""
        self.status_label.setText(message)
        self.fetch_button.setEnabled(True)
        self.progress_bar.setValue(0)

    def show_error_and_close(self, message: str):
        """Show error message and optionally close application after delay."""
        self.status_label.setText(message)
        if AUTO_CLOSE_AFTER_WALLPAPER:
            QTimer.singleShot(AUTO_CLOSE_DELAY_MS, self.close)
        else:
            # Change status to indicate manual mode
            QTimer.singleShot(2000, lambda: self.status_label.setText("Error occurred - App ready for manual use"))

    def closeEvent(self, event):
        """Handle application close event."""
        # Clean up worker threads
        if self.fetch_worker and self.fetch_worker.isRunning():
            self.fetch_worker.terminate()
            self.fetch_worker.wait()

        if self.download_worker and self.download_worker.isRunning():
            self.download_worker.terminate()
            self.download_worker.wait()

        event.accept()
