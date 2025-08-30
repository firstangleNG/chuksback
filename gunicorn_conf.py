from multiprocessing import cpu_count

# Socket Path
bind = 'unix:/var/www/home/chuk_user/chuk/chukticketingsystem/gunicorn.sock'

# Worker Options
workers = cpu_count() + 1
worker_class = 'sync'  # Use default sync worker for WSGI/Django

# Logging Options
loglevel = 'debug'
accesslog = '/var/www/home/chuk_user/chuk/chukticketingsystem/access_log'
errorlog = '/var/www/home/chuk_user/chuk/chukticketingsystem/error_log'
