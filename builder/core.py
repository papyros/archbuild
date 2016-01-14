import os
import os.path

import redis
from celery import Celery, Task
from celery.utils.log import get_task_logger
from github3 import login


class Container(object):
    objects = []

    def get(self, name):
        return next((obj for obj in self.objects if obj.name == name), None)


class JobTask(Task):
    status = 'Not yet started'


class Object(object):
    name = None
    status = 'Not yet built'
    

base_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
workdir = os.path.join(base_dir, 'working')
chroots_dir = os.path.join(base_dir, 'chroots')
server_url = 'http://b2f7f6ee.ngrok.io'

celery = Celery('builder')
celery.config_from_object('config')
celery.Task = JobTask

logger = get_task_logger('builder')

redis_client = redis.Redis()


token = id = ''
with open(os.path.join(base_dir, '.github_auth'), 'r') as fd:
    token = fd.readline().strip()  # Can't hurt to be paranoid
    id = fd.readline().strip()

gh = login(token=token)

if not gh:
    raise Exception('Unable to sign into GitHub!')
