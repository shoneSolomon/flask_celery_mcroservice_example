
dir:
app: the code area
base_service: the microservice base of connection( a module base of swagger)

流程：

先启动redis，我用docker启动的

cd flask_celery_mcroservice_example
export OPENAPI_CONFIG_PATH=/your_root_path/flask_celery_mcroservice_example/base_service/openapi.yaml

先启动celery, 此处同目录：cmd窗口
celery worker -A task.celery -l info

如果@celery.task(bind=True)在app.py里面：
celery worker -A app.celery -l debug -E
如果@celery.task(bind=True)在和app同级目录的task.py：
celery worker -A task.celery -l info
如果在其他模块：
celery -A application.controllers.routes:celery worker --loglevel=info
celery -A app.api.endpoints.simple_check  worker --loglevel=info
celery -A app.async_tasks.tasks worker --loglevel=info
celery -A app.api.endpoints.user_posts.celery  worker --loglevel=info

启动另一个窗口启动flask:
uwsgi --http :20000 -w app.main

接口celery测试：
测试：
我的路由是：<br>创建任务：
post  http://localhost:20000/testing
request:
application/json
{url="xxxxx.jpg"}

response:
"task_id": "44057af4-3e14-468a-a36d-8c31e3665bce"

带着返回的task_id取回结果
get http://localhost:20000/testing/{task_id}

response:
 {
        "id": "44057af4-3e14-468a-a36d-8c31e3665bc",
        "ready": true,
        "result": [
            "http://s3.xxxx.com/ba7571a95d64eaa69a49912f26816e2f.jpg",
            60,
            "helloworld"
        ],
        "state": "SUCCESS",
        "status": "SUCCESS"
 }

