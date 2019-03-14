from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from flask_mongoengine import MongoEngine
from elasticsearch import Elasticsearch
from celery import Celery

from ..main import app

mysql_store = SQLAlchemy(app.app)
redis_store = FlaskRedis(app.app)
mongo_store = MongoEngine(app.app)
es_store = Elasticsearch(app.app.config['ES_HOSTS'])

