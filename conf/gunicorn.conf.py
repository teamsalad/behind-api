import multiprocessing


bind = 'unix:/var/run/gunicorn.sock'
worker_class = 'gevent'
worker_connections = (multiprocessing.cpu_count() * 2 + 1) * 1000
workers = multiprocessing.cpu_count() * 2 + 1

