"""
WSGI config for TimeTrackerBackend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from modules.rpc_client_pool import RPCClientPool

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TimeTrackerBackend.settings')

application = get_wsgi_application()

# As this is singleton it will be initialized there. It will start threads that will monitor things.
rpc_pool = RPCClientPool()
