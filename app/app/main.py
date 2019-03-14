# coding=utf-8

import connexion
import os

app = connexion.FlaskApp(__name__, specification_dir='.')


application = app.app
# Celery configuration db 8
application.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/8'
application.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/8'
app.add_api(os.environ.get('OPENAPI_CONFIG_PATH', 'openapi.yaml'), validate_responses=True)


if __name__ == "__main__":
    app.run(debug=True, port=10003)



