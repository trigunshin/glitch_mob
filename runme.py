from celery import Celery

celery = Celery('glitch_mob.runme')#, include=['glitch_mob.tasks'])
celery.config_from_object('celeryconfig')

if __name__ == '__main__':
    celery.start()
