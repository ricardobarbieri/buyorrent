@echo off
echo Parando todos os processos do Streamlit...
taskkill /F /IM streamlit.exe
taskkill /F /IM python.exe
echo.
echo Processos encerrados.
pause