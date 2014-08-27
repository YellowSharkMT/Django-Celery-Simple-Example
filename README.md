## Simple Django + Celery/RabbitMQ Example

The purpose of this example is to provide a minimal, working baseline for using Django with Celery and RabbitMQ. This example does not intend to show a production-ready project, its goal is to highlight the basic configuration options and allow the user to see how these three components work together. 

This project is based on the following versions:

- Django 1.6.6
- Celery 3.1.13
- RabbitMQ 3.2.4
- Ubuntu 14.04

### Setup:

You must have RabbitMQ installed (`sudo apt-get install rabbitmq-server`). First, create a user named `rmq_user`, password `abc123`, and a vhost named `rmd_host`:

    $ sudo rabbitmqctl add_user rmq_user abc123
    $ sudo rabbitmqctl add_vhost rmq_host
    $ sudo rabbitmqctl set_permissions -p rmq_host rmq_user ".*" ".*" ".*"

Next, clone this repository and set up the environment:

    $ git clone (repo url) 
    $ cd dj_test_app/
    $ mkvirtualenv dj_test_app # <-- command assumes virtualenvwrapper
    $ (venv) pip install django celery django-celery

Next, synchronize Django's database & verify that Django runs correctly:

    $ (venv) python manage.py syncdb # for this project, there's no need to add an administrator
    $ (venv) python manage.py runserver

You should have no errors at this point, and you should be able to reach the Django start page by visiting http://127.0.0.1:8000 in your browser. Setting up Django is beyond the scope of this project, see [the official docs on installing Django](https://docs.djangoproject.com/en/1.6/intro/install/) for more information.

If successful, the next steps are to start the Celery workers/queues, and send them some tasks. (For reference, see the files `dj_test_app/celery.py`, and `dj_test_app/tasks.py`). The next commands will each require their own terminal window, as you will be running celery in "worker" mode, not in daemonized mode. 

Open two new terminal windows, and in each one, navigate to the project root, and activate the virtualenv.

    $ # NEW TERMINAL 1, will run the "default" queue.
    $ workon dj_test_app
    $ cd [project root]
    $ (venv) celery -A dj_test_app worker -l info -Q default -n default

    $ # NEW TERMINAL 2, will run the "high" queue.
    $ workon dj_test_app
    $ cd [project root]
    $ (venv) celery -A dj_test_app worker -l info -Q high -n high

After executing those commands, Celery should produce some information output and enter a running state. The last line of that output should look like:

    [2014-08-27 13:54:36,274: WARNING/MainProcess] celery@high ready.

Future activity from these workers will be logged to these windows. At this point, you'll want to watch out for some initial exceptions, especially related to not being able to reach the broker (RabbitMQ). Double-check that you are using the correct RabbitMQ username, password and vhost from the commands above. Those values are configured in the `dj_test_app/settings.py` file. If your setup is correct, you should have no further entries in the logged output, at this point.

Now to see Django and Celery in action together, you can now open up the Django shell, and launch some tasks (use the first terminal window you had open, prior to launching the new ones for the celery tasks. Or open up a new terminal, navigate to the project root, and activate your virtualenv). 

In the `dj_test_app/tasks.py` file, there are two tasks: `add`, and `multiply`. Import them, and run them via `.delay()`, or `.apply_async()`. While running these commands, be sure that you can observe the output for the celery workers.

    $ (venv) python manage.py shell
    >>> from dj_test_app.tasks import add, multiply
    >>> add(4,6) # executes immediately / does not get queued
    10
    >>> add.delay(4,6) # will be queued to the "default" queue
    <AsyncResult: abc-123-some-hash-here>
    >>> add.apply_async(args=[4,6], queue='high') # task will be executed by the "high" queue
    <AsyncResult: abc-123-some-hash-here>

    >>> for _ in range(30): # <- lets fire off a whole bunch of tasks...
    ...   add.delay(1,2)    
    ...   multiply.apply_async([4,5], queue='high')
    ...   multiply.apply_async([8,3], queue='high')
    ...   multiply.apply_async([6,2], queue='default')
    <AsyncResult: abc-123-some-hash-here> (several of these)

While executing those examples, you should be able to observe those tasks being directed to the specified queue. 

## Configuration Information

- Modifications to `settings.py` file:
-- TODO
- New file: `celery.py`
-- TODO
- New file: `tasks.py`
-- TODO

## Links to Resources

TODO
