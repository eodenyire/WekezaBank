@echo off
echo 🚀 SQLite to MySQL Migration Tool
echo ================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python first: https://python.org
    pause
    exit /b 1
)

REM Install required packages
echo 📦 Installing required packages...
pip install pandas mysql-connector-python sqlalchemy

REM Run migration
echo 🔄 Starting migration...
python quick_migrate.py

echo.
echo ✅ Migration completed!
pause