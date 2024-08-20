"""
ASGI config for DESAFIO_AT_INOA_DJANGO project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DESAFIO_AT_INOA_DJANGO.settings')

application = get_asgi_application()
