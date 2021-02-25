from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
import json
from datetime import date

from . import errors, service


@csrf_exempt
def admin_auth(request: HttpRequest):
    """ Документация """

    if request.method != "POST":
        return Response(errors.HTTP_405, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return Response(errors.HTTP_400_JSON, status=status.HTTP_400_BAD_REQUEST)

    if any([
        data['username'] is None,
        data['password'] is None,

        not isinstance(data['username'], str),
        not isinstance(data['password'], str)
    ]):
        return Response(errors.HTTP_401, status=status.HTTP_401_UNAUTHORIZED)

    response, err = service.admin_auth(request, data['username'], data['password'])

    if err:
        return Response(errors.HTTP_500, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(response, status=status.HTTP_200_OK)


@csrf_exempt
def poll_create(request: HttpRequest):
    """ Документация """

    if request.method != "POST":
        return Response(errors.HTTP_405, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return Response(errors.HTTP_400_JSON, status=status.HTTP_400_BAD_REQUEST)

    if any([
        data['name'] is None,
        data['date_start'] is None,
        data['date_end'] is None,
        data['description'] is None,

        # Нельзя указать время начала раньше времени окончания
        (
                isinstance(data['date_start'], date) and
                isinstance(data['date_end'], date) and
                data['date_end'] < data['date_start']
        ),

        not isinstance(data['name'], str),
        not isinstance(data['description'], str)
    ]):
        return Response(errors.HTTP_400_WRONG_PARAMS, status=status.HTTP_400_BAD_REQUEST)

    response, err = service.poll_create(
        request, data['name'], data['date_start'], data['date_end'], data['description']
    )

    if err:
        return Response(errors.HTTP_500, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(response, status=status.HTTP_200_OK)


@csrf_exempt
def poll_update(request: HttpRequest):
    """ Документация """

    if request.method != "POST":
        return Response(errors.HTTP_405, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return Response(errors.HTTP_400_JSON, status=status.HTTP_400_BAD_REQUEST)

    if any([
        data['poll_id'] is None,
        not isinstance(data['poll_id'], int) or data['poll_id'] <= 0,

        'name' in data and not isinstance(data['name'], str),
        'date_end' in data and not isinstance(data['date_end'], date),
        'description' in data and not isinstance(data['description'], str)
    ]):
        return Response(errors.HTTP_400_WRONG_PARAMS, status=status.HTTP_400_BAD_REQUEST)

    # БИЗНЕС-ЛОГИКА
    # poll_id должен существовать
    # name должен быть также уникальным при обновлении
    # date_end не должен быть меньше стартового при обновлении

    # response = json
    # error = bool (False default)
    response, err = service.poll_update(data['poll_id'], data['name'], data['date_end'], data['description'])

    if err:
        return Response(errors.HTTP_500, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(response, status=status.HTTP_200_OK)


@csrf_exempt
def poll_delete(request: HttpRequest):
    """ Документация """

    if request.method != "POST":
        return Response(errors.HTTP_405, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return Response(errors.HTTP_400_JSON, status=status.HTTP_400_BAD_REQUEST)

    # poll_id
    if any([
        data['poll_id'] is None,
        not isinstance(data['poll_id'], int) or data['poll_id'] <= 0
    ]):
        return Response(errors.HTTP_400_WRONG_PARAMS, status=status.HTTP_400_BAD_REQUEST)

    # БИЗНЕС-ЛОГИКА
    # poll_id должен существовать

    # response = json
    # error = bool (False default)
    response, err = service.poll_delete(request, data['poll_id'])

    if err:
        return Response(errors.HTTP_500, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(response, status=status.HTTP_200_OK)


@csrf_exempt
def question_create(request: HttpRequest):
    """ Документация """

    if request.method != "POST":
        return Response(errors.HTTP_405, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return Response(errors.HTTP_400_JSON, status=status.HTTP_400_BAD_REQUEST)

    if any([
        data['poll_id'] is None,
        not isinstance(data['poll_id'], int) or data['poll_id'] <= 0,

        'text' in data and not isinstance(data['text'], str),
        'type' in data and data['type'] not in ('t', 'c', 'r'),

        'answers' in data and not isinstance(data['answers'], list)
    ]):
        return Response(errors.HTTP_400_WRONG_PARAMS, status=status.HTTP_400_BAD_REQUEST)

    answers = data.get('answers')

    # БИЗНЕС-ЛОГИКА
    # poll_id должен существовать

    # response = json
    # error = bool (False default)
    response, err = service.question_create(request, data['poll_id'], data['text'], data['type'], answers)

    if err:
        return Response(errors.HTTP_500, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(response, status=status.HTTP_200_OK)


@csrf_exempt
def question_update(request: HttpRequest):
    """ Документация """

    if request.method != "POST":
        return Response(errors.HTTP_405, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return Response(errors.HTTP_400_JSON, status=status.HTTP_400_BAD_REQUEST)

    if any([
        data['q_id'] is None,
        not isinstance(data['q_id'], int) or data['q_id'] <= 0,

        'text' in data and not isinstance(data['text'], str),
        'type' in data and data['type'] not in ('t', 'c', 'r'),

        'answers' in data and not isinstance(data['answers'], list)
    ]):
        return Response(errors.HTTP_400_WRONG_PARAMS, status=status.HTTP_400_BAD_REQUEST)

    answers = data.get('answers')

    # Проверить соответствие типа ответов с переданными ответами в JSON
    # ИЛИ можно любые ответы передавать в списке, а потом, в зависимости от типа, извлекать

    # БИЗНЕС-ЛОГИКА

    # response = json
    # error = bool (False default)
    response, err = service.question_update(request, data['q_id'], data['text'], data['type'], answers)

    if err:
        return Response(errors.HTTP_500, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(response, status=status.HTTP_200_OK)


@csrf_exempt
def question_delete(request: HttpRequest):
    """ Документация """

    if request.method != "POST":
        return Response(errors.HTTP_405, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return Response(errors.HTTP_400_JSON, status=status.HTTP_400_BAD_REQUEST)

    # q_id
    if any([
        data['q_id'] is None,
        not isinstance(data['q_id'], int) or data['q_id'] <= 0
    ]):
        return Response(errors.HTTP_400_WRONG_PARAMS, status=status.HTTP_400_BAD_REQUEST)

    # БИЗНЕС-ЛОГИКА

    # response = json
    # error = bool (False default)
    response, err = service.question_delete(request, data['q_id'])

    if err:
        return Response(errors.HTTP_500, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(response, status=status.HTTP_200_OK)


@csrf_exempt
def get_active_polls(request: HttpRequest):
    """ Документация """

    if request.method != 'POST':
        return Response(errors.HTTP_405, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return Response(errors.HTTP_400_JSON, status=status.HTTP_400_BAD_REQUEST)

    if any([
        data['page'] is None,
        not isinstance(data['page'], int) or data['page'] <= 0
    ]):
        return Response(errors.HTTP_400_WRONG_PARAMS, status=status.HTTP_400_BAD_REQUEST)

    response, err = service.get_active_polls(data['page'])

    if err:
        return Response(errors.HTTP_500, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(response, status=status.HTTP_200_OK)


@csrf_exempt
def complete_poll(request: HttpRequest):
    """ Документация """

    if request.method != "POST":
        return Response(errors.HTTP_405, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return Response(errors.HTTP_400_JSON, status=status.HTTP_400_BAD_REQUEST)

    if any([
        data['user_id'] is None,
        not isinstance(data['user_id'], int) or data['user_id'] <= 0,

        data['poll_id'] is None,
        not isinstance(data['poll_id'], int) or data['poll_id'] <= 0,

        'answers' in data and not isinstance(data['answers'], list)
    ]):
        return Response(errors.HTTP_400_WRONG_PARAMS, status=status.HTTP_400_BAD_REQUEST)

    answers = data.get('answers')

    # Извлечь ответ в соответствии с типом (или как это вообще взаимодействует с бизнес-логикой?)
    # БИЗНЕС-ЛОГИКА

    # response = json
    # error = bool (False default)
    response, err = service.complete_poll(data['user_id'], data['poll_id'], answers)

    if err:
        return Response(errors.HTTP_500, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(response, status=status.HTTP_200_OK)


@csrf_exempt
def get_done_polls(request: HttpRequest):
    if request.method != "POST":
        return Response(errors.HTTP_405, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return Response(errors.HTTP_400_JSON, status=status.HTTP_400_BAD_REQUEST)

    if any([
        data['user_id'] is None,
        not isinstance(data['user_id'], int) or data['user_id'] <= 0,

        data['page'] is None,
        not isinstance(data['page'], int) or data['page'] <= 0
    ]):
        return Response(errors.HTTP_400_WRONG_PARAMS, status=status.HTTP_400_BAD_REQUEST)

    # БИЗНЕС-ЛОГИКА

    # response = json
    # error = bool (False default)
    response, err = service.get_done_polls(data['user_id'], data['page'])

    if err:
        return Response(errors.HTTP_500, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(response, status=status.HTTP_200_OK)
