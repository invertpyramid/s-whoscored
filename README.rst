======================
A Spider for WhoScored
======================

This is a scrapy project for WhoScored_ web scraping.

.. _WhoScored: https://www.whoscored.com/

Overview
========

.. image:: https://mperlet.github.io/pybadge/badges/9.41.svg
    :alt: pylint Score

.. image:: https://circleci.com/gh/invertpyramid/s-whoscored/tree/master.svg?style=svg
    :target: https://circleci.com/gh/invertpyramid/s-whoscored/tree/master

.. image:: https://img.shields.io/badge/License-GPLv3-blue.svg
    :target: https://www.gnu.org/licenses/gpl-3.0
    :alt: License: AGPL v3

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/python/black
    :alt: Code style: black

Requirements
============

.. image:: https://pyup.io/repos/github/invertpyramid/s-whoscored/python-3-shield.svg
   :target: https://pyup.io/repos/github/invertpyramid/s-whoscored/
   :alt: Python 3

.. image:: https://pyup.io/repos/github/invertpyramid/s-whoscored/shield.svg
   :target: https://pyup.io/repos/github/invertpyramid/s-whoscored/
   :alt: pyup

.. image:: https://snyk.io/test/github/invertpyramid/s-whoscored/badge.svg
    :target: https://snyk.io/test/github/invertpyramid/s-whoscored
    :alt: Known Vulnerabilities

.. image:: https://img.shields.io/badge/renovate-enabled-brightgreen.svg
    :target: https://renovatebot.com
    :alt: Renovate enabled

* Python 3.6+
* Scrapy 1.6.0
* Fully tested on Linux, but it should works on Windows, Mac OSX, BSD

Usage
=====

Run Sentry
----------

Initial postgres with senty first:

1. Generate secret key first:
::
    docker run --rm sentry config generate-secret-key

2. Use the secret key to create a database in postgres:
::
    docker run --detach \
        --name sentry-redis-init \
        --volume $PWD/redis-data:/data \
        redis
    docker run --detach \
        --name sentry-postgres-init \
        --env POSTGRES_PASSWORD=secret \
        --env POSTGRES_USER=sentry \
        --volume $PWD/postgres-data:/var/lib/postgresql/data \
        postgres
    docker run --interactive --tty --rm \
        --env SENTRY_SECRET_KEY='<secret-key>' \
        --link sentry-postgres-init:postgres \
        --link sentry-redis-init:redis \
        sentry upgrade

Then input the superusername and password

3. Stop the redis and postgres:
::
    docker stop sentry-postgres-init sentry-redis-init && docker rm sentry-postgres-init senty-redis-init

4. Edit the env files to add the superusername, password and database related
   information

5. Start sentry with docker-compose.yml:
::
    docker-compose up --detach && docker-compose logs --follow

Run MongoDB for httpcache
-------------------------

Run Percona Server MongoDB for cookies
--------------------------------------

Debug with mitmproxy
====================

Start mitmproxy
---------------

Enable httpproxy middleware
---------------------------

Debug in mitmproxy
------------------

TODO
====

