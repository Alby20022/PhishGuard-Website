@echo off
echo ========================================================
echo PhishGuard - Push to GitHub
echo ========================================================
echo.
echo This script will help you push your code to GitHub.
echo.

:ask_url
set /p repo_url="Please paste your new GitHub Repository URL (e.g., https://github.com/Alby20022/PhishGuard.git): "
if "%repo_url%"=="" goto ask_url

echo.
echo Adding remote origin...
git remote remove origin 2>nul
git remote add origin %repo_url%

echo.
echo Renaming branch to main...
git branch -M main

echo.
echo Pushing to GitHub...
echo (You may be asked to sign in via browser or token)
git push -u origin main

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Push failed. Please check the URL and your internet connection.
    pause
    exit /b %errorlevel%
)

echo.
echo [SUCCESS] Code pushed successfully!
pause
