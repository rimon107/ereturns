ereturns
========

This portal is used for uploading and downloading data.


Basic Commands
--------------

Install Packages
^^^^^^^^^^^^^^^^

Installing package using the following command:

::

  $ pip install package_name

Running Commands Using Docker
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

command:

::

  $ python manage.py runserver 0.0.0.0:8000

Deployment
----------

The following details how to deploy this application.

Deploy
^^^^^^

For local development:

::

  $ command



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
