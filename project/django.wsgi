import os
import sys
import django.core.handlers.wsgi
sys.path.append(r'F:/project')
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
application = django.core.handlers.wsgi.WSGIHandler()