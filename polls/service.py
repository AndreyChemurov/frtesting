from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.db import transaction
from django.db.models import Q

from datetime import date

from polls.models import *


@transaction.atomic
def admin_auth(request, username: str, password: str):
    err = False

    admin = get_user_model()

    if not admin.objects.filter(username=username).exists():
        transaction.rollback()

        err = True
        return None, err

    user = authenticate(request, username=username, password=password)

    if user is None:
        transaction.rollback()

        err = True
        return None, err

    login(request, user)

    transaction.commit()

    return {"login": "success"}, err


@transaction.atomic
def poll_create(request, name: str, date_start: date, date_end: date, description: str):
    err = False

    if not request.user.is_authenticated:
        transaction.rollback()

        err = True
        return None, err

    new_poll = Polls(name=name, date_start=date_start, date_end=date_end, description=description)
    new_poll.save()

    transaction.commit()

    return {"create_poll": "success"}, err


@transaction.atomic
def poll_update(request, poll_id: int, name: str = None, date_end: date = None, description: str = None):
    err = False

    if not request.user.is_authenticated:
        transaction.rollback()

        err = True
        return None, err

    if not Polls.objects.filter(pk=poll_id):
        transaction.rollback()

        err = True
        return None, err

    poll_to_upd = Polls.objects.get(pk=poll_id)

    if name:
        poll_to_upd.name = name

    if date_end:
        poll_to_upd.date_end = date_end

    if description:
        poll_to_upd.description = description

    poll_to_upd.save()

    transaction.commit()

    return {"update_poll": "success"}, err


@transaction.atomic
def poll_delete(request, poll_id: int):
    err = False

    if not request.user.is_authenticated:
        transaction.rollback()

        err = True
        return None, err

    Polls.objects.filter(pk=poll_id).delete()

    transaction.commit()

    return {"delete_poll": "success"}, err


@transaction.atomic
def question_create(request, poll_id: int, text: str, _type: str, answers: list = None):
    err = False

    if not request.user.is_authenticated:
        transaction.rollback()

        err = True
        return None, err

    if not Polls.objects.filter(pk=poll_id):
        transaction.rollback()

        err = True
        return None, err

    q = Questions(poll_id=poll_id, text=text, type=_type)
    q.save()

    if _type in ('r', 'c'):
        for ans in answers:
            a = PollPossibleAnswers(q_id=q.id, text=ans)
            a.save()
    else:
        a = PollPossibleAnswers(q_id=q.id, text=None)
        a.save()

    transaction.commit()

    return {"create_question": "success"}, err


@transaction.atomic
def question_update(request, q_id: int, text: str, _type: str, answers: list = None):
    err = False

    if not request.user.is_authenticated:
        transaction.rollback()

        err = True
        return None, err

    if not Questions.objects.filter(pk=q_id):
        transaction.rollback()

        err = True
        return None, err

    q_to_upd = Questions.objects.get(pk=q_id)

    if text:
        q_to_upd.text = text

    # Придумать как обновить тип и вместе с ним ответы

    transaction.commit()

    return {"update_question": "success"}, err


@transaction.atomic
def question_delete(request, q_id: int):
    err = False

    if not request.user.is_authenticated:
        transaction.rollback()

        err = True
        return None, err

    Questions.objects.filter(pk=q_id).delete()

    transaction.commit()

    return {"delete_question": "success"}, err


@transaction.atomic
def get_active_polls(page: int):
    # err = False
    #
    # today = date.today()
    # active_polls = Polls.objects.filter(Q(date_end__gte=today)|Q(date_end=None))
    #
    # if not active_polls:
    #     err = True
    #     return None, err
    #
    # return active_polls, err
    pass


@transaction.atomic
def complete_poll(user_id: int, poll_id: int, answers: list = None):
    pass


@transaction.atomic
def get_done_polls(user_id: int, page: int):
    pass
