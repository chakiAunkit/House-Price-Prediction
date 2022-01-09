@ECHO OFF 
:: This batch files runs python scripts for the required repo
TITLE Python Initialize
ECHO Please wait... 
:: Section 1: venv
ECHO Initializing Virtual Environment
python -m venv env
./env/Scripts/activate.bat
