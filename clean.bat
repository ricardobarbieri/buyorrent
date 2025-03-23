@echo off
echo Limpando instalacao...
echo.

:: Parar processos
taskkill /F /IM streamlit.exe 2>nul
taskkill /F /IM python.exe 2>nul

:: Remover ambiente virtual
rmdir /s /q venv 2>nul

:: Remover cache
rmdir /s /q __pycache__ 2>nul
rmdir /s /q .streamlit 2>nul

echo Limpeza concluida!
echo Execute setup.bat para uma nova instalacao.
pause