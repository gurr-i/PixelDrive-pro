"""
Custom UI widgets for enhanced user experience.
"""

import os
from typing import Optional
from PyQt5.QtWidgets import (
    QLabel, QFrame, QVBoxLayout, QHBoxLayout, QWidget, 
    QGraphicsDropShadowEffect, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import QPixmap, QMovie, QPainter, QPen, QColor, QFont


class LoadingSpinner(QLabel):
    """Animated loading spinner widget."""
    
    def __init__(self, size: int = 32, parent=None):
        super().__init__(parent)
        self.size = size
        self.angle = 0
        self.setFixedSize(size, size)
        self.setAlignment(Qt.AlignCenter)
        
        # Animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate)
        
    def start_animation(self):
        """Start the spinning animation."""
        self.timer.start(50)  # Update every 50ms
        
    def stop_animation(self):
        """Stop the spinning animation."""
        self.timer.stop()
        
    def rotate(self):
        """Rotate the spinner."""
        self.angle = (self.angle + 10) % 360
        self.update()
        
    def paintEvent(self, event):
        """Custom paint event for the spinner."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Set up the pen
        pen = QPen(QColor(0, 120, 212), 3)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        
        # Draw the spinner
        rect = self.rect().adjusted(5, 5, -5, -5)
        painter.translate(rect.center())
        painter.rotate(self.angle)
        
        # Draw arcs
        for i in range(8):
            alpha = 255 - (i * 30)
            pen.setColor(QColor(0, 120, 212, alpha))
            painter.setPen(pen)
            painter.drawLine(0, -rect.height()//2 + 5, 0, -rect.height()//2 + 15)
            painter.rotate(45)


class ImagePreviewCard(QFrame):
    """Enhanced image preview card with loading states."""
    
    def __init__(self, width: int = 300, height: int = 200, parent=None):
        super().__init__(parent)
        self.setFixedSize(width, height)
        self.setProperty("class", "card")
        
        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        
        # Image container
        self.image_container = QFrame()
        self.image_container.setFixedSize(width - 16, height - 60)
        
        # Image label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setProperty("class", "image-preview")
        self.image_label.setFixedSize(width - 32, height - 76)
        
        # Loading spinner
        self.loading_spinner = LoadingSpinner(32)
        self.loading_spinner.hide()
        
        # Placeholder
        self.placeholder_label = QLabel("📷\nClick to preview")
        self.placeholder_label.setAlignment(Qt.AlignCenter)
        self.placeholder_label.setProperty("class", "placeholder")
        self.placeholder_label.setFixedSize(width - 32, height - 76)
        
        # Info label
        self.info_label = QLabel("Select an image")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setProperty("class", "subtitle")
        self.info_label.setWordWrap(True)
        
        # Container layout
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(self.placeholder_label)
        container_layout.addWidget(self.image_label)
        container_layout.addWidget(self.loading_spinner, 0, Qt.AlignCenter)
        self.image_container.setLayout(container_layout)
        
        layout.addWidget(self.image_container)
        layout.addWidget(self.info_label)
        self.setLayout(layout)
        
        # Initially show placeholder
        self.show_placeholder()
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        
    def show_placeholder(self):
        """Show placeholder state."""
        self.placeholder_label.show()
        self.image_label.hide()
        self.loading_spinner.hide()
        self.loading_spinner.stop_animation()
        self.info_label.setText("Select an image")
        
    def show_loading(self, message: str = "Loading..."):
        """Show loading state."""
        self.placeholder_label.hide()
        self.image_label.hide()
        self.loading_spinner.show()
        self.loading_spinner.start_animation()
        self.info_label.setText(message)
        
    def show_image(self, pixmap: QPixmap, info: str = ""):
        """Show loaded image."""
        self.placeholder_label.hide()
        self.loading_spinner.hide()
        self.loading_spinner.stop_animation()
        self.image_label.show()
        
        # Scale pixmap to fit
        scaled_pixmap = pixmap.scaled(
            self.image_label.size(), 
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)
        self.info_label.setText(info)
        
    def show_error(self, message: str = "Failed to load image"):
        """Show error state."""
        self.placeholder_label.show()
        self.placeholder_label.setText("❌\nFailed to load")
        self.image_label.hide()
        self.loading_spinner.hide()
        self.loading_spinner.stop_animation()
        self.info_label.setText(message)


class EnhancedListWidget(QListWidget):
    """Enhanced list widget with better styling and animations."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setVerticalScrollMode(QListWidget.ScrollPerPixel)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setSpacing(4)
        
    def add_photo_item(self, photo_data: dict, thumbnail_pixmap: Optional[QPixmap] = None):
        """Add a photo item with enhanced styling."""
        # Create custom widget for the item
        item_widget = QWidget()
        item_widget.setFixedHeight(80)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(12)
        
        # Thumbnail
        thumbnail_label = QLabel()
        thumbnail_label.setFixedSize(64, 64)
        thumbnail_label.setAlignment(Qt.AlignCenter)
        thumbnail_label.setProperty("class", "image-preview")
        
        if thumbnail_pixmap and not thumbnail_pixmap.isNull():
            scaled_thumb = thumbnail_pixmap.scaled(
                64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            thumbnail_label.setPixmap(scaled_thumb)
        else:
            thumbnail_label.setText("📷")
            thumbnail_label.setProperty("class", "placeholder")
        
        # Info section
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        # Author name
        author_name = photo_data.get('user', {}).get('name', 'Unknown')
        author_label = QLabel(author_name)
        author_label.setProperty("class", "title")
        author_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        
        # Photo description or dimensions
        description = photo_data.get('description', '')
        if not description:
            width = photo_data.get('width', 0)
            height = photo_data.get('height', 0)
            description = f"{width} × {height}" if width and height else "High resolution"
        
        desc_label = QLabel(description[:50] + "..." if len(description) > 50 else description)
        desc_label.setProperty("class", "subtitle")
        desc_label.setWordWrap(True)
        
        info_layout.addWidget(author_label)
        info_layout.addWidget(desc_label)
        info_layout.addStretch()
        
        layout.addWidget(thumbnail_label)
        layout.addLayout(info_layout)
        layout.addStretch()
        
        item_widget.setLayout(layout)
        
        # Create list item
        item = QListWidgetItem()
        item.setSizeHint(item_widget.sizeHint())
        item.setData(Qt.UserRole, photo_data)
        
        self.addItem(item)
        self.setItemWidget(item, item_widget)
        
        return item
