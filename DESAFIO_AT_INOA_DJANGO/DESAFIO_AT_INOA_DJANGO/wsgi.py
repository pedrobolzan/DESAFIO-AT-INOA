"""
WSGI config for DESAFIO_AT_INOA_DJANGO project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DESAFIO_AT_INOA_DJANGO.DESAFIO_AT_INOA_DJANGO.settings')

#os.environ.setdefault('RUNNING_AS_WSGI', 'True')

application = get_wsgi_application()
