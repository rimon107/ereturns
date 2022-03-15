ereturns
========

This portal is used for uploading and downloading data.


Basic Commands
--------------

Install Packages
^^^^^^^^^^^^^^^^

Installing package using the following command:

::

  $ docker-compose -f file.yml run --rm django pip install package_name

Running Commands Using Docker
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

command:

::

  $ docker-compose -f local.yml run --rm django python manage.py command
  $ docker-compose -f local.yml up --build
  $ docker-compose -f local.yml run --rm django python manage.py makemigrations
  $ docker-compose -f local.yml run --rm django python manage.py migrate
  $ docker-compose -f local.yml exec django /bin/bash
  $ docker-compose -f local.yml exec postgres /bin/bash
  $ docker-compose -f local.yml exec postgres backups
  $ docker cp $(docker-compose -f local.yml ps -q postgres):/backups ./backups
  $ docker-compose -f local.yml exec postgres restore backup_2018_03_13T09_05_07.sql.gz

Deployment
----------

The following details how to deploy this application.

Docker
^^^^^^

For local development:

::

  $ docker-compose -f local.yml up --build

For production:

::

  $ docker-compose -f production.yml up --build


Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy ereturns

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest


Celery
^^^^^^

This app comes with Celery.

To run a celery worker:

.. code-block:: bash

    cd ereturns
    celery -A config.celery_app worker -l info

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.

rimon
Admin@1234
