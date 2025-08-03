"""
GUI styling and themes for the wallpaper changer application.
Enhanced with modern UI elements, loading states, and premium styling.
"""


class DarkTheme:
    """Dark theme styling for the application."""
    
    @staticmethod
    def get_stylesheet() -> str:
        """
        Get the dark theme stylesheet.
        
        Returns:
            CSS-like stylesheet string for PyQt5 application
        """
        return """
            QMainWindow {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #1A1A1A, stop: 1 #0F0F0F);
                border: none;
            }
            QWidget {
                background-color: transparent;
                color: #E0E0E0;
                font-family: 'Segoe UI', 'San Francisco', 'Helvetica Neue', Arial, sans-serif;
                font-size: 14px;
                font-weight: 400;
            }
            QLineEdit, QComboBox {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #2A2A2A, stop: 1 #252525);
                border: 1px solid #404040;
                border-radius: 8px;
                padding: 10px 12px;
                color: #E0E0E0;
                font-size: 14px;
                selection-background-color: #0078D4;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #0078D4;
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #2F2F2F, stop: 1 #2A2A2A);
                box-shadow: 0 0 10px rgba(0, 120, 212, 0.3);
            }
            QLineEdit:hover, QComboBox:hover {
                border: 1px solid #505050;
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #2F2F2F, stop: 1 #2A2A2A);
            }
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #0078D4, stop: 1 #0063B1);
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                color: white;
                font-weight: 600;
                font-size: 14px;
                min-height: 16px;
                box-shadow: 0 2px 8px rgba(0, 120, 212, 0.3);
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #0063B1, stop: 1 #005A9E);
                box-shadow: 0 4px 12px rgba(0, 120, 212, 0.4);
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #005A9E, stop: 1 #004B87);
                box-shadow: 0 1px 4px rgba(0, 120, 212, 0.2);
                transform: translateY(0px);
            }
            QPushButton:disabled {
                background: #404040;
                color: #808080;
                box-shadow: none;
            }
            QProgressBar {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #2A2A2A, stop: 1 #252525);
                border: 1px solid #404040;
                border-radius: 8px;
                height: 12px;
                text-align: center;
                color: #E0E0E0;
                font-weight: 500;
                font-size: 12px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #00C853, stop: 0.5 #00E676, stop: 1 #00C853);
                border-radius: 6px;
                box-shadow: 0 0 10px rgba(0, 200, 83, 0.3);
            }

            /* Loading spinner styles */
            QLabel[class="loading-spinner"] {
                background: transparent;
                border: 3px solid #404040;
                border-top: 3px solid #0078D4;
                border-radius: 50%;
                width: 24px;
                height: 24px;
            }

            /* Card container styles */
            QFrame[class="card"] {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #2A2A2A, stop: 1 #252525);
                border: 1px solid #404040;
                border-radius: 12px;
                padding: 16px;
                margin: 8px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            }

            /* Preview image styles */
            QLabel[class="image-preview"] {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #2A2A2A, stop: 1 #1F1F1F);
                border: 2px solid #404040;
                border-radius: 12px;
                padding: 8px;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
            }

            /* Placeholder styles */
            QLabel[class="placeholder"] {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #2A2A2A, stop: 0.5 #353535, stop: 1 #2A2A2A);
                border: 2px dashed #505050;
                border-radius: 12px;
                color: #808080;
                font-size: 16px;
                font-weight: 500;
            }
            QLabel {
                color: #B0B0B0;
                font-weight: 400;
            }
            QLabel[class="title"] {
                color: #FFFFFF;
                font-size: 18px;
                font-weight: 600;
                margin: 8px 0px;
            }
            QLabel[class="subtitle"] {
                color: #A0A0A0;
                font-size: 12px;
                font-weight: 400;
            }
            QListWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #252525, stop: 1 #1F1F1F);
                border: 1px solid #404040;
                border-radius: 12px;
                padding: 8px;
                outline: none;
            }
            QListWidget::item {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #2A2A2A, stop: 1 #252525);
                border: 1px solid #404040;
                border-radius: 8px;
                padding: 12px;
                margin: 4px;
                color: #E0E0E0;
                font-weight: 500;
            }
            QListWidget::item:selected {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #0078D4, stop: 1 #0063B1);
                border: 1px solid #0078D4;
                color: #FFFFFF;
                box-shadow: 0 2px 8px rgba(0, 120, 212, 0.3);
            }
            QListWidget::item:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #353535, stop: 1 #2F2F2F);
                border: 1px solid #505050;
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            }
            QComboBox QAbstractItemView {
                background-color: #252525;
                border: 1px solid #404040;
                selection-background-color: #0078D4;
                color: #E0E0E0;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #E0E0E0;
                margin-right: 5px;
            }
            QScrollBar:vertical {
                background-color: #2D2D2D;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #404040;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #505050;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """


class LightTheme:
    """Light theme styling for the application."""
    
    @staticmethod
    def get_stylesheet() -> str:
        """
        Get the light theme stylesheet.
        
        Returns:
            CSS-like stylesheet string for PyQt5 application
        """
        return """
            QMainWindow {
                background-color: #FFFFFF;
            }
            QWidget {
                background-color: #FFFFFF;
                color: #2D2D2D;
                font-family: Segoe UI;
                font-size: 14px;
            }
            QLineEdit, QComboBox, QListWidget {
                background-color: #F5F5F5;
                border: 1px solid #CCCCCC;
                border-radius: 6px;
                padding: 6px;
                color: #2D2D2D;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #0078D4;
            }
            QPushButton {
                background-color: #0078D4;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                color: white;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #0063B1;
            }
            QPushButton:pressed {
                background-color: #005A9E;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
                color: #808080;
            }
            QProgressBar {
                background-color: #F5F5F5;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                height: 8px;
            }
            QProgressBar::chunk {
                background-color: #00C853;
                border-radius: 4px;
            }
            QLabel {
                color: #555555;
            }
            QListWidget::item {
                padding: 4px;
                border-bottom: 1px solid #E0E0E0;
            }
            QListWidget::item:selected {
                background-color: #E3F2FD;
                color: #1976D2;
            }
            QListWidget::item:hover {
                background-color: #F5F5F5;
            }
            QComboBox QAbstractItemView {
                background-color: #FFFFFF;
                border: 1px solid #CCCCCC;
                selection-background-color: #0078D4;
                color: #2D2D2D;
            }
        """
