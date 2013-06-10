glitch_mob
==========

# Redis #
http://docs.celeryproject.org/en/latest/getting-started/brokers/redis.html

    pip install celery
    pip install -U celery-with-redis
    BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
