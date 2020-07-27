from django.contrib.auth import logout
from django.contrib.auth.models import AnonymousUser
from komax_app.models import Worker
from django.shortcuts import get_object_or_404, redirect

def logout_view(request, *args, **kwargs):
    user = request.user
    if user is not AnonymousUser:
        if user.groups.filter(name='Operator'):
            worker = get_object_or_404(Worker, user=user)
            worker.current_komax = None
            worker.save()
        logout(request)
    return redirect('login')


