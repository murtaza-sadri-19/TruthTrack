# gunicorn_config.py

import multiprocessing

# Worker configuration
workers = multiprocessing.cpu_count() * 2 + 1  # Dynamic number of workers based on CPU cores
worker_class = 'sync'  # Worker class to use
threads = 2  # Number of threads per worker
timeout = 120  # Worker timeout in seconds

# Binding
bind = "0.0.0.0:10000"  # IP and port to bind to

# Logging
accesslog = '-'  # Log to stdout
errorlog = '-'  # Log to stderr
loglevel = 'info'

# Process naming
proc_name = 'truthtrack'  # Process name

# Max requests and timeout
max_requests = 1000
max_requests_jitter = 50
graceful_timeout = 30

# Application specific
preload_app = True

# Reload on code changes (disable in production)
reload = False