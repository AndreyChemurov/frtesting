from django.db import models


class Polls(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False, null=False)
    name = models.CharField(max_length=200, unique=True, null=False)
    date_start = models.DateField(editable=False, null=False)
    date_end = models.DateField(editable=True, null=False)
    description = models.TextField(editable=True, null=False)


class Questions(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False, null=False)
    poll_id = models.ForeignKey(Polls, on_delete=models.DO_NOTHING)
    text = models.TextField(editable=True, null=False)
    type = models.CharField(max_length=1, editable=True, null=False)


# Варианты ответа на конкретный вопрос
class PollPossibleAnswers(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False, null=False)
    q_id = models.ForeignKey(Questions, on_delete=models.DO_NOTHING)
    text = models.TextField(editable=True, null=True)   # null, если ответ открытый (пользовательская строка)


# Пользовательские ответы на конкретный вопрос
class UserAnswers(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False, null=False)
    user_id = models.BigIntegerField(editable=False, null=False)
    q_id = models.ForeignKey(Questions, on_delete=models.DO_NOTHING)    # На какой вопрос
    user_ans = models.ForeignKey(PollPossibleAnswers, on_delete=models.DO_NOTHING)  # Какой вариант ответа

    # Если отвечашь на текстовый вопрос, то это пишется сюда
    # Если вопрос с типом 'r' или 'c', то здесь будет null
    text_ans = models.TextField(editable=False, null=True)
