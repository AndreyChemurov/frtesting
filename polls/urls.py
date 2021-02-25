from django.urls import path

from . import views

urlpatterns = [
    path('admin/auth', views.admin_auth, name='admin_auth'),
    path('admin/poll/create', views.poll_create, name='poll_create'),
    path('admin/poll/update', views.poll_update, name='poll_update'),
    path('admin/poll/delete', views.poll_delete, name='poll_delete'),
    path('admin/question/create', views.question_create, name='question_create'),
    path('admin/question/update', views.question_update, name='question_update'),
    path('admin/question/delete', views.question_delete, name='question_delete'),

    path('users/polls/active', views.get_active_polls, name='get_active_polls'),
    path('users/polls/complete', views.complete_poll, name='complete_poll'),
    path('users/polls/get', views.get_done_polls, name='get_done_polls'),
]
