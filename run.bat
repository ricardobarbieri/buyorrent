@echo off
echo ====================================
echo Iniciando Simulador de Financiamento
echo ====================================
echo.

:: Ativar ambiente virtual
call venv\Scripts\activate

:: Executar a aplicação
echo Iniciando aplicacao...
echo Aguarde, seu navegador sera aberto automaticamente...
echo.
streamlit run app.py

:: Desativar ambiente virtual ao fechar
call venv\Scripts\deactivate

pause