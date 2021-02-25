from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import status
import json

from . import errors, service


@csrf_exempt
def admin_auth(request):
    """
    Метод авторизации пользователя.
    Входные данные:
        1. username: имя пользователя (админ назначен "frtesting")
        2. password: пароль (для админа "frtesting")
    """

    # Проверка валидности метода
    if request.method != "POST":
        return JsonResponse(errors.HTTP_405, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # Извлечение данных из запроса
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(errors.HTTP_400_JSON, status=status.HTTP_400_BAD_REQUEST)

    # Проверка валидности входных данных
    if any([
        'username' not in data or not isinstance(data['username'], str),
        'password' not in data or not isinstance(data['password'], str),
    ]):
        return JsonResponse(errors.HTTP_400_WRONG_PARAMS, status=status.HTTP_400_BAD_REQUEST)

    # Проверить, что имя админа валидное
    if data['username'] != "frtesting":
        return JsonResponse(errors.HTTP_401, status=status.HTTP_401_UNAUTHORIZED)

    """
        Вызов соответствующей функции из бизнес-логики.
        response: ответ бизнес-логики, dict.
        err: bool тип данных, сообщяющий транспортному уровню, что что-то пошло не так.
    """
    response, err = service.admin_auth(request, data['username'], data['password'])

    if err:
        return JsonResponse(errors.HTTP_500, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JsonResponse(response, status=status.HTTP_200_OK)


@csrf_exempt
def poll_create(request):
    """
    Метод создания нового опроса.
    Входные данные:
        1. name: уникальне имя опроса.
        2. date_start: дата начала опроса
        3. date_end: дата окончания опроса
        4. description: описание опроса
    Возвращаемые значения:
        1. id: уникальный идентификатор созданного опроса.
    """

    # Проверка валидности метода
    if request.method != "POST":
        return JsonResponse(errors.HTTP_405, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # Извлечение данных из запроса
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(errors.HTTP_400_JSON, status=status.HTTP_400_BAD_REQUEST)

    # Проверка валидности входных данных
    if any([
        'name' not in data or not isinstance(data['name'], str),
        'description' not in data or not isinstance(data['description'], str),
    ]):
        return JsonResponse(errors.HTTP_400_WRONG_PARAMS, status=status.HTTP_400_BAD_REQUEST)

    """
            Вызов соответствующей функции из бизнес-логики.
            response: ответ бизнес-логики, dict.
            err: bool тип данных, сообщяющий транспортному уровню, что что-то пошло не так.
    """
    response, err = service.poll_create(
        request, data['name'], data['date_start'], data['date_end'], data['description']
    )

    if err:
        return JsonResponse(errors.HTTP_500, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JsonResponse(response, status=status.HTTP_200_OK)


@csrf_exempt
def poll_update(request):
    """
    Метод изменения содержимого опроса.
    Входные данные:
        1. poll_id: уникальный id опроса, который нужно изменить
        2. name: название опроса
        3. date_end: дата окончания опроса
        4. description: описание опроса
    Возвращаемые значения:
        1. id: идентификатор измененного объявления
    """

    # Проверка валидности метода
    if request.method != "POST":
        return JsonResponse(errors.HTTP_405, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # Извлечение данных из запроса
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(errors.HTTP_400_JSON, status=status.HTTP_400_BAD_REQUEST)

    """
            Вызов соответствующей функции из бизнес-логики.
            response: ответ бизнес-логики, dict.
            err: bool тип данных, сообщяющий транспортному уровню, что что-то пошло не так.
    """
    response, err = service.poll_update(request, data['poll_id'], data['name'], data['date_end'], data['description'])

    if err:
        return JsonResponse(errors.HTTP_500, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JsonResponse(response, status=status.HTTP_200_OK)


@csrf_exempt
def poll_delete(request):
    """
    Метод удаления опроса.
    Входные данные:
        1. poll_id: идентификатор удаляемого опроса.
    Выходные значения:
        1. poll_id: идентификатор удаленного опроса.
    """

    # Проверка валидности метода
    if request.method != "POST":
        return JsonResponse(errors.HTTP_405, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # Извлечение данных из запроса
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(errors.HTTP_400_JSON, status=status.HTTP_400_BAD_REQUEST)

    # Проверка валидности входных данных
    if any([
        data['poll_id'] is None,
        not isinstance(data['poll_id'], int) or data['poll_id'] <= 0
    ]):
        return JsonResponse(errors.HTTP_400_WRONG_PARAMS, status=status.HTTP_400_BAD_REQUEST)

    """
            Вызов соответствующей функции из бизнес-логики.
            response: ответ бизнес-логики, dict.
            err: bool тип данных, сообщяющий транспортному уровню, что что-то пошло не так.
    """
    response, err = service.poll_delete(request, data['poll_id'])

    if err:
        return JsonResponse(errors.HTTP_500, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JsonResponse(response, status=status.HTTP_200_OK)


@csrf_exempt
def question_create(request):
    """
    Метод создания вопроса к опросу.
    Входные данные:
        1. poll_id: идентификатор опроса, к которому относится вопрос.
        2. text: текст вопроса
        3. type: тип вопроса
        4. answers: варианты ответа
    Возвращаемые значения:
        1. q_id: идентификатор созданного вопроса
    """

    # Проверка валидности метода
    if request.method != "POST":
        return JsonResponse(errors.HTTP_405, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # Извлечение данных из запроса
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(errors.HTTP_400_JSON, status=status.HTTP_400_BAD_REQUEST)

    # Проверка валидности входных данных
    if any([
        data['poll_id'] is None,
        not isinstance(data['poll_id'], int) or data['poll_id'] <= 0,

        'text' in data and not isinstance(data['text'], str),
        'type' in data and data['type'] not in ('t', 'c', 'r'),

        'answers' in data and not isinstance(data['answers'], list)
    ]):
        return JsonResponse(errors.HTTP_400_WRONG_PARAMS, status=status.HTTP_400_BAD_REQUEST)

    answers = data.get('answers')

    """
            Вызов соответствующей функции из бизнес-логики.
            response: ответ бизнес-логики, dict.
            err: bool тип данных, сообщяющий транспортному уровню, что что-то пошло не так.
    """
    response, err = service.question_create(request, data['poll_id'], data['text'], data['type'], answers)

    if err:
        return JsonResponse(errors.HTTP_500, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JsonResponse(response, status=status.HTTP_200_OK)


@csrf_exempt
def question_update(request):
    """
    Метод изменения вопроса.
    Входные данные:
        1. q_id: идентификатор вопроса
        2. text: текст вопроса
        3. type: тип вопроса
        4. answers: варианты ответа
    Возвращаемые значения:
        1. q_id: идентификатор измененног вопроса
    """

    # Проверка валидности метода
    if request.method != "POST":
        return JsonResponse(errors.HTTP_405, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # Извлечение данных из запроса
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(errors.HTTP_400_JSON, status=status.HTTP_400_BAD_REQUEST)

    # Проверка валидности входных данных
    if any([
        data['q_id'] is None,
        not isinstance(data['q_id'], int) or data['q_id'] <= 0,

        'text' in data and not isinstance(data['text'], str),
        'type' in data and data['type'] not in ('t', 'c', 'r'),

        'answers' in data and not isinstance(data['answers'], list)
    ]):
        return JsonResponse(errors.HTTP_400_WRONG_PARAMS, status=status.HTTP_400_BAD_REQUEST)

    answers = data.get('answers')

    """
            Вызов соответствующей функции из бизнес-логики.
            response: ответ бизнес-логики, dict.
            err: bool тип данных, сообщяющий транспортному уровню, что что-то пошло не так.
    """
    response, err = service.question_update(request, data['q_id'], data['text'], data['type'], answers)

    if err:
        return JsonResponse(errors.HTTP_500, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JsonResponse(response, status=status.HTTP_200_OK)


@csrf_exempt
def question_delete(request):
    """
    Метод удаления вопроса.
    Входные данные:
        1. q_id: уникальный идентификатор вопроса
    Выходные значения:
        1. q_id: уникальный идентификатор удаленного вопроса
    """

    # Проверка валидности метода
    if request.method != "POST":
        return JsonResponse(errors.HTTP_405, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # Извлечение данных из запроса
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(errors.HTTP_400_JSON, status=status.HTTP_400_BAD_REQUEST)

    # Проверка валидности входных данных
    if any([
        data['q_id'] is None,
        not isinstance(data['q_id'], int) or data['q_id'] <= 0
    ]):
        return JsonResponse(errors.HTTP_400_WRONG_PARAMS, status=status.HTTP_400_BAD_REQUEST)

    """
            Вызов соответствующей функции из бизнес-логики.
            response: ответ бизнес-логики, dict.
            err: bool тип данных, сообщяющий транспортному уровню, что что-то пошло не так.
    """
    response, err = service.question_delete(request, data['q_id'])

    if err:
        return JsonResponse(errors.HTTP_500, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JsonResponse(response, status=status.HTTP_200_OK)


@csrf_exempt
def get_active_polls(request):
    """ Метод получения активных опросов. """

    # Проверка валидности метода
    if request.method != 'GET':
        return JsonResponse(errors.HTTP_405, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    """
            Вызов соответствующей функции из бизнес-логики.
            response: ответ бизнес-логики, dict.
            err: bool тип данных, сообщяющий транспортному уровню, что что-то пошло не так.
    """
    response, err = service.get_active_polls()

    if err:
        return JsonResponse(errors.HTTP_500, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JsonResponse(response, status=status.HTTP_200_OK, safe=False)


@csrf_exempt
def complete_poll(request):
    """
    Метод ответа на вопрос.
    Входные данные:
        1. user_id: пользовательский id
        2. q_id: идентификатор вопроса, на котороый отвечает пользователь
        3. answers: ответ(ы) на вопрос
    """

    # Проверка валидности метода
    if request.method != "POST":
        return JsonResponse(errors.HTTP_405, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # Извлечение данных из запроса
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(errors.HTTP_400_JSON, status=status.HTTP_400_BAD_REQUEST)

    # Проверка валидности входных данных
    if any([
        data['user_id'] is None,
        not isinstance(data['user_id'], int) or data['user_id'] <= 0,

        data['q_id'] is None,
        not isinstance(data['q_id'], int) or data['q_id'] <= 0,

        'answers' in data and not isinstance(data['answers'], list)
    ]):
        return JsonResponse(errors.HTTP_400_WRONG_PARAMS, status=status.HTTP_400_BAD_REQUEST)

    answers = data.get('answers')

    """
            Вызов соответствующей функции из бизнес-логики.
            response: ответ бизнес-логики, dict.
            err: bool тип данных, сообщяющий транспортному уровню, что что-то пошло не так.
    """
    response, err = service.complete_poll(data['user_id'], data['q_id'], answers)

    if err:
        return JsonResponse(errors.HTTP_500, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JsonResponse(response, status=status.HTTP_200_OK)


@csrf_exempt
def get_done_polls(request):
    """
    Метод получения выполненных пользователем опросов.
    """

    # Проверка валидности метода
    if request.method != "POST":
        return JsonResponse(errors.HTTP_405, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # Извлечение данных из запроса
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(errors.HTTP_400_JSON, status=status.HTTP_400_BAD_REQUEST)

    # Проверка валидности входных данных
    if any([
        data['user_id'] is None,
        not isinstance(data['user_id'], int) or data['user_id'] <= 0
    ]):
        return JsonResponse(errors.HTTP_400_WRONG_PARAMS, status=status.HTTP_400_BAD_REQUEST)

    """
            Вызов соответствующей функции из бизнес-логики.
            response: ответ бизнес-логики, dict.
            err: bool тип данных, сообщяющий транспортному уровню, что что-то пошло не так.
    """
    response, err = service.get_done_polls(data['user_id'])

    if err:
        return JsonResponse(errors.HTTP_500, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JsonResponse(response, status=status.HTTP_200_OK, safe=False)
