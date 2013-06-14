## Broker settings.
BROKER_URL = "amqp://glitch_mob:gm@kilrog.dyndns.org//gmob"

# List of modules to import when celery starts.
CELERY_IMPORTS = ("tasks", "ticker_cid_map")

## Using the database to store task state and results.
#CELERY_RESULT_BACKEND = "redis"
CELERY_RESULT_BACKEND = 'redis://kilrog.dyndns.org:6379/0'

CELERY_ANNOTATIONS = {"glitch_mob.tasks.add": {"rate_limit": "10/s"}}
#CELERYD_CONCURRENCY = 1
CELERYD_PREFETCH_MULTIPLIER = 4

#CELERY_TASK_SERIALIZER = 'json'
