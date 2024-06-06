echo -e "pip start install requirements\n"
pip3 install -r requirements.txt
echo -e "creating database models"
python3 init_db.py
echo -e "running scrapper"
python3 scrapper.py
python3 main.py
