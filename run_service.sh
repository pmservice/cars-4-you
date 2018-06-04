source activate py35env
pip install -r requirements.txt
export FLASK_APP=server.py
flask run