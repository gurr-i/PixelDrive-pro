@echo off
echo Starting Wallpaper Changer...
echo.

REM Try to run the new modular version first
if exist "dist\Wallpaper Changer.exe" (
    echo Running new modular version...
    "dist\Wallpaper Changer.exe"
) else if exist "wallpaper_changer\main.py" (
    echo Running from source...
    python -m wallpaper_changer.main
) else if exist "startupwallpaper.py" (
    echo Running legacy version...
    python startupwallpaper.py
) else (
    echo Error: No wallpaper changer found!
    pause
    exit /b 1
)

echo.
echo Wallpaper Changer finished.
pause
