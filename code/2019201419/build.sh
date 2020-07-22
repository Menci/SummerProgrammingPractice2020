service redis-server start
python3 backend/crawling.py
python3 backend/index_maker.py
python3 manage.py runserver