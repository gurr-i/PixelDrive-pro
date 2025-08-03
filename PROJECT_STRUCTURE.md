# Project Structure Overview

This document provides a comprehensive overview of the refactored Wallpaper Changer project structure.

## Directory Structure

```
wallpaper_changer/                    # Root project directory
├── wallpaper_changer/               # Main package
│   ├── __init__.py                  # Package initialization
│   ├── config.py                    # Configuration and constants
│   ├── main.py                      # Main entry point
│   ├── api/                         # API handling modules
│   │   ├── __init__.py
│   │   └── unsplash.py             # Unsplash API client
│   ├── workers/                     # Background worker threads
│   │   ├── __init__.py
│   │   ├── fetch_worker.py         # Photo fetching worker
│   │   └── download_worker.py      # Photo download worker
│   ├── gui/                         # GUI components
│   │   ├── __init__.py
│   │   ├── styles.py               # UI themes and styling
│   │   └── main_window.py          # Main application window
│   └── utils/                       # Utility modules
│       ├── __init__.py
│       └── wallpaper.py            # Wallpaper management utilities
├── examples/                        # Usage examples
│   └── basic_usage.py              # Programmatic API usage example
├── requirements.txt                 # Python dependencies
├── setup.py                        # Package installation script
├── README.md                       # Project documentation
├── CHANGELOG.md                    # Version history
├── .gitignore                      # Git ignore rules
└── startupwallpaper.py             # Legacy compatibility script
```

## Module Descriptions

### Core Package (`wallpaper_changer/`)

#### `__init__.py`
- Package initialization with version info
- Exports main package metadata

#### `config.py`
- Centralized configuration management
- API keys and endpoints
- File paths and directories
- UI constants and settings
- Logging configuration

#### `main.py`
- Main application entry point
- Logging setup
- Application lifecycle management

### API Module (`wallpaper_changer/api/`)

#### `unsplash.py`
- `UnsplashAPI` class for API interactions
- Photo search functionality
- Download management with progress tracking
- Enhanced error handling with custom exceptions
- Type hints for better code quality

### Workers Module (`wallpaper_changer/workers/`)

#### `fetch_worker.py`
- `FetchWorker` class extending `QThread`
- Asynchronous photo fetching from Unsplash
- Signal-based communication with main thread

#### `download_worker.py`
- `DownloadWorker` class extending `QThread`
- Asynchronous photo downloading
- Progress reporting and thumbnail generation

### GUI Module (`wallpaper_changer/gui/`)

#### `styles.py`
- `DarkTheme` and `LightTheme` classes
- Centralized UI styling
- CSS-like stylesheets for PyQt5

#### `main_window.py`
- `WallpaperApp` main window class
- Complete UI implementation
- Event handling and user interactions
- Integration with workers and utilities

### Utils Module (`wallpaper_changer/utils/`)

#### `wallpaper.py`
- `WallpaperManager` class for cross-platform wallpaper setting
- Windows, macOS, and Linux support
- Desktop and lockscreen wallpaper management
- Platform-specific error handling

## Key Improvements

### 1. Modular Architecture
- **Before**: Single 436-line monolithic script
- **After**: 13 focused modules with clear responsibilities
- **Benefits**: Better maintainability, testability, and reusability

### 2. Enhanced Error Handling
- Custom exception classes (`UnsplashAPIError`)
- Detailed error messages with context
- Platform-specific error handling
- Proper logging throughout the application

### 3. Type Safety
- Type hints added throughout the codebase
- Better IDE support and code completion
- Reduced runtime errors

### 4. Configuration Management
- Centralized configuration in `config.py`
- Environment variable support
- Easy customization without code changes

### 5. Package Management
- Proper `setup.py` for installation
- `requirements.txt` for dependencies
- Console script entry point

### 6. Documentation
- Comprehensive docstrings
- Usage examples
- Installation and setup instructions

### 7. Backward Compatibility
- Original script still works
- Deprecation warnings for migration
- Smooth transition path

## Usage Methods

### 1. New Modular Way (Recommended)
```bash
# Run directly
python -m wallpaper_changer.main

# Or install and use console script
pip install -e .
wallpaper-changer
```

### 2. Programmatic Usage
```python
from wallpaper_changer.api import UnsplashAPI
from wallpaper_changer.utils import WallpaperManager

api = UnsplashAPI()
photos = api.search_photos("Tesla")
# ... use the API programmatically
```

### 3. Legacy Compatibility
```bash
# Still works but shows deprecation warning
python startupwallpaper.py
```

## Testing

All modules can be imported and tested independently:

```bash
# Test individual modules
python -c "from wallpaper_changer.config import GENRES; print('✅ Config OK')"
python -c "from wallpaper_changer.api import UnsplashAPI; print('✅ API OK')"
python -c "from wallpaper_changer.workers import FetchWorker; print('✅ Workers OK')"
python -c "from wallpaper_changer.gui import WallpaperApp; print('✅ GUI OK')"
python -c "from wallpaper_changer.utils import WallpaperManager; print('✅ Utils OK')"
```

## Migration Benefits

1. **Maintainability**: Easier to modify and extend individual components
2. **Testability**: Each module can be unit tested independently
3. **Reusability**: Components can be used in other projects
4. **Scalability**: Easy to add new features without affecting existing code
5. **Code Quality**: Better organization, type safety, and documentation
6. **Professional Structure**: Follows Python packaging best practices
