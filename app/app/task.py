
import connexion
from celery import Celery

app = connexion.FlaskApp(__name__, specification_dir='.')

application = app.app
# Celery configuration db 8
application.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/8'
application.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/8'


def make_celery(app):
    celery = Celery(app.name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app.app)


@celery.task(bind=True)
def calling_api(self, url):

    # try:
    #     lenth = len(url)
    # except SomeNetworkException as e:
    #     print("maybe do some clenup here....")
    # self.retry(e)

    result = [url, len(url), "helloworld"]
    return result


