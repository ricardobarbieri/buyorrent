@echo off
echo ====================================
echo Configurando ambiente do simulador
echo ====================================
echo.

:: Verificar se Python está instalado
python --version > nul 2>&1
if errorlevel 1 (
    echo Python nao encontrado! Por favor, instale o Python 3.8 ou superior.
    echo Voce pode baixar em: https://www.python.org/downloads/
    pause
    exit
)

:: Criar ambiente virtual
echo Criando ambiente virtual...
python -m venv venv
echo.

:: Ativar ambiente virtual
echo Ativando ambiente virtual...
call venv\Scripts\activate
echo.

:: Instalar dependências
echo Instalando dependencias...
pip install -r requirements.txt
echo.

echo ====================================
echo Configuracao concluida com sucesso!
echo ====================================
echo Para executar o programa, use o arquivo run.bat
echo.
pause