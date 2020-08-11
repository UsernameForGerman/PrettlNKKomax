from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from .models import Worker

class WorkerAuthBackend(ModelBackend):
    """
    Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

    Use the login name and a hash of the password. For example:

    ADMIN_LOGIN = 'admin'
    ADMIN_PASSWORD = 'pbkdf2_sha256$30000$Vo0VlMnkR4Bk$qEvtdyZRWTcOsCnI/oQ7fVOu1XAURIZYoOZ3iq8Dr4M='
    """

    def authenticate(self, request, email=None, password=None, *args, **kwargs):
        try:
            worker = Worker.objects.get(email=email)
            pwd_valid = check_password(password, worker.password)
            if pwd_valid:
                return worker
            else:
                return None
        except Worker.DoesNotExist:
            return None

    def get_user(self, worker_id):
        try:
            return Worker.objects.get(id=worker_id)
        except Worker.DoesNotExist:
            return None