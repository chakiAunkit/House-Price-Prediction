ECHO ==============================
ECHO Installing modules
ECHO ==============================
export PYTHONPATH=$PWD
pip install -r requirements.txt
ECHO ===============================
ECHO Installed. Launching server on port 8080
ECHO ===============================
uvicorn main:app --reload
START http://localhost:8080/docs
PAUSE