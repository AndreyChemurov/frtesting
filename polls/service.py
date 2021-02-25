from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.contrib.auth.models import User
from django.db import transaction
from django.db import connection
from datetime import date

from polls.models import *


@transaction.non_atomic_requests
def admin_auth(request, username: str, password: str):
    err = False

    admin = get_user_model()

    if not admin.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email='', password=password)

    user = authenticate(request, username=username, password=password)

    if user is None:
        transaction.rollback()

        err = True
        return None, err

    login(request, user)

    transaction.commit()

    return {"login": "success"}, err


@transaction.non_atomic_requests
def poll_create(request, name: str, date_start: date, date_end: date, description: str):
    err = False

    if not request.user.is_authenticated:
        transaction.rollback()

        err = True
        return None, err

    new_poll = Polls(name=name, date_start=date_start, date_end=date_end, description=description)
    new_poll.save()

    transaction.commit()

    print(new_poll)

    return {"poll_id": new_poll.id}, err


@transaction.non_atomic_requests
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

    poll_to_upd = Polls.objects.filter(pk=poll_id)[0]

    if name:
        poll_to_upd.name = name

    if date_end:
        poll_to_upd.date_end = date_end

    if description:
        poll_to_upd.description = description

    poll_to_upd.save()

    transaction.commit()

    print(poll_to_upd)

    return {"poll_id": poll_id}, err


@transaction.non_atomic_requests
def poll_delete(request, poll_id: int):
    err = False

    if not request.user.is_authenticated:
        transaction.rollback()

        err = True
        return None, err

    poll_to_delete = Polls.objects.filter(pk=poll_id)[0]

    if not poll_to_delete:
        transaction.rollback()

        err = True
        return None, err

    poll_to_delete.delete()

    transaction.commit()

    print(poll_to_delete)

    return {"poll_id": poll_id}, err


@transaction.non_atomic_requests
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

    poll = Polls.objects.filter(pk=poll_id)[0]

    q = Questions(poll_id=poll, text=text, type=_type)
    q.save()

    if _type in ('r', 'c'):
        for ans in answers:
            question = Questions.objects.filter(pk=q.id)[0]
            a = PollPossibleAnswers(q_id=question, text=ans)
            a.save()
            print(a)
    else:
        question = Questions.objects.filter(pk=q.id)[0]
        a = PollPossibleAnswers(q_id=question, text=None)
        a.save()
        print(a)

    q.save()
    transaction.commit()

    print(q)

    return {"create_question": q.id}, err


@transaction.non_atomic_requests
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

    q_to_upd = Questions.objects.filter(pk=q_id)[0]

    if text:
        q_to_upd.text = text

    if _type:
        q_to_upd.type = _type

    if _type in ('r', 'c'):
        for ans in answers:
            question = Questions.objects.filter(pk=q_id)[0]
            a = PollPossibleAnswers(q_id=question, text=ans)
            a.save()
            print(a)
    else:
        question = Questions.objects.filter(pk=q_id)[0]
        a = PollPossibleAnswers(q_id=question, text=None)
        a.save()
        print(a)

    transaction.commit()

    print(q_to_upd)

    return {"update_question": q_id}, err


@transaction.non_atomic_requests
def question_delete(request, q_id: int):
    err = False

    if not request.user.is_authenticated:
        transaction.rollback()

        err = True
        return None, err

    q_to_delete = Questions.objects.filter(pk=q_id)[0]

    if not q_to_delete:
        transaction.rollback()

        err = True
        return None, err

    q_to_delete.delete()

    transaction.commit()

    print(q_to_delete)
    print(PollPossibleAnswers.objects.filter(q_id=q_id))

    return {"delete_question": q_id}, err


@transaction.non_atomic_requests
def get_active_polls():
    err = False

    today = date.today()
    active_polls = Polls.objects.filter(Q(date_end__gte=today) | Q(date_end=None)).values()

    if not active_polls:
        err = True
        return None, err

    return list(active_polls), err


@transaction.non_atomic_requests
def complete_poll(user_id: int, q_id: int, answers: list = None):
    err = False

    q = Questions.objects.filter(pk=q_id)[0]
    pa = PollPossibleAnswers.objects.filter(pk=answers[0])[0]

    user_ans = UserAnswers(user_id=user_id, q_id=q, user_ans=pa, text_ans=answers[1])
    user_ans.save()

    transaction.commit()

    print(user_ans)

    return {"q_id_answer": q_id}, err


@transaction.non_atomic_requests
def get_done_polls(user_id: int):
    # TODO: NOT IMPLEMENTED

    polls = Questions.objects.raw('''SELECT DISTINCT "poll_id"
    FROM "questions" q INNER JOIN "user_answers" u
    ON ("user_id"=%s AND q.id=u.q_id);''', [user_id])

    return None, False
