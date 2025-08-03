#!/usr/bin/env python3
"""
Test script for the enhanced UI features.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_enhanced_components():
    """Test all enhanced UI components."""
    print("🧪 Testing Enhanced UI Components")
    print("=" * 40)
    
    tests_passed = 0
    total_tests = 6
    
    # Test 1: Custom widgets import
    try:
        from wallpaper_changer.gui.widgets import LoadingSpinner, ImagePreviewCard, EnhancedListWidget
        print("✅ 1. Custom widgets import successful")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ 1. Custom widgets import failed: {e}")
    
    # Test 2: Enhanced styles import
    try:
        from wallpaper_changer.gui.styles import DarkTheme, LightTheme
        dark_style = DarkTheme.get_stylesheet()
        light_style = LightTheme.get_stylesheet()
        print("✅ 2. Enhanced styles import successful")
        print(f"   📊 Dark theme: {len(dark_style)} characters")
        print(f"   📊 Light theme: {len(light_style)} characters")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ 2. Enhanced styles import failed: {e}")
    
    # Test 3: Main window with enhancements
    try:
        from wallpaper_changer.gui import WallpaperApp
        print("✅ 3. Enhanced main window import successful")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ 3. Enhanced main window import failed: {e}")
    
    # Test 4: PyQt5 components
    try:
        from PyQt5.QtWidgets import QApplication, QLabel
        from PyQt5.QtCore import QTimer
        from PyQt5.QtGui import QPixmap
        print("✅ 4. PyQt5 components available")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ 4. PyQt5 components failed: {e}")
    
    # Test 5: Configuration with new features
    try:
        from wallpaper_changer.config import AUTO_CLOSE_AFTER_WALLPAPER, APP_ICON_PATH
        print("✅ 5. Enhanced configuration available")
        print(f"   🔧 Auto-close: {AUTO_CLOSE_AFTER_WALLPAPER}")
        print(f"   🎨 Icon path: {os.path.basename(APP_ICON_PATH)}")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ 5. Enhanced configuration failed: {e}")
    
    # Test 6: Executable exists
    try:
        exe_path = "dist/Wallpaper Changer.exe"
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print("✅ 6. Enhanced executable available")
            print(f"   📁 Size: {size_mb:.1f} MB")
            tests_passed += 1
        else:
            print("❌ 6. Enhanced executable not found")
    except Exception as e:
        print(f"❌ 6. Executable check failed: {e}")
    
    # Summary
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {tests_passed}/{total_tests} passed")
    
    if tests_passed == total_tests:
        print("🎉 All enhanced UI tests passed!")
        print("\n🚀 Ready to use:")
        print("   • Enhanced UI with modern design")
        print("   • Loading states and animations")
        print("   • Premium styling and interactions")
        print("   • Professional user experience")
        return True
    else:
        print("❌ Some enhanced UI tests failed!")
        return False

def test_ui_features():
    """Test specific UI features."""
    print("\n🎨 Testing UI Feature Integration")
    print("-" * 40)
    
    try:
        # Test loading spinner
        from wallpaper_changer.gui.widgets import LoadingSpinner
        spinner = LoadingSpinner(32)
        print("✅ Loading spinner creation successful")
        
        # Test image preview card
        from wallpaper_changer.gui.widgets import ImagePreviewCard
        preview = ImagePreviewCard(300, 200)
        print("✅ Image preview card creation successful")
        
        # Test enhanced list widget
        from wallpaper_changer.gui.widgets import EnhancedListWidget
        list_widget = EnhancedListWidget()
        print("✅ Enhanced list widget creation successful")
        
        print("✅ All UI components can be instantiated")
        return True
        
    except Exception as e:
        print(f"❌ UI feature test failed: {e}")
        return False

if __name__ == "__main__":
    print("🎨 Enhanced UI Test Suite")
    print("=" * 50)
    
    component_test = test_enhanced_components()
    feature_test = test_ui_features()
    
    if component_test and feature_test:
        print("\n🎊 Enhanced UI is ready!")
        print("💡 Run 'python demo_enhanced_ui.py' to see it in action")
        sys.exit(0)
    else:
        print("\n❌ Enhanced UI tests failed!")
        sys.exit(1)
