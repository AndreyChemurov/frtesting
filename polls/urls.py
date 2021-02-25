from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('admin/auth', csrf_exempt(views.admin_auth), name='admin_auth'),
    path('admin/poll/create', csrf_exempt(views.poll_create), name='poll_create'),
    path('admin/poll/update', csrf_exempt(views.poll_update), name='poll_update'),
    path('admin/poll/delete', csrf_exempt(views.poll_delete), name='poll_delete'),
    path('admin/question/create', csrf_exempt(views.question_create), name='question_create'),
    path('admin/question/update', csrf_exempt(views.question_update), name='question_update'),
    path('admin/question/delete', csrf_exempt(views.question_delete), name='question_delete'),

    path('users/polls/active', csrf_exempt(views.get_active_polls), name='get_active_polls'),
    path('users/polls/complete', csrf_exempt(views.complete_poll), name='complete_poll'),
    path('users/polls/get', csrf_exempt(views.get_done_polls), name='get_done_polls'),
]
