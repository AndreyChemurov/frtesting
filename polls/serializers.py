from rest_framework import serializers
from polls.models import (
    User,
    Poll
)


class UserSerializer(serializers.Serializer):
    pass


class PollSerializer(serializers.Serializer):
    pass
