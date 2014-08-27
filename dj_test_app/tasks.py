from __future__ import absolute_import
from celery import task

def add(x,y):
  return x + y

@task
def multiply(x,y):
  return x * y

@task
def pause():
  import time
  time.sleep(1.5)
  return 'DONE SLEEPING'
