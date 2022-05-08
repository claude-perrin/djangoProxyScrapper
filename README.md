# djangotest

To run:
1) Activate environment: source /env/bin/activate
2) Django: python manager.py runserver
3) Redis: redis-server
4) Start Celery beating: celery -A Proxies beat -l INFO
5) Listening to beats: celery -A Proxies worker -l info --pool=solo
