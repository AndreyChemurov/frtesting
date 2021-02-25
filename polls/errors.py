from rest_framework import status

HTTP_405 = {
    "error": {
        "detail": "Method not allowed",
        "status": status.HTTP_405_METHOD_NOT_ALLOWED
    }
}

HTTP_400_JSON = {
    "error": {
        "detail": "Bad JSON format",
        "status": status.HTTP_400_BAD_REQUEST
    }
}

HTTP_400_WRONG_PARAMS = {
    "error": {
        "detail": "Wrong or missed body parameters",
        "status": status.HTTP_400_BAD_REQUEST
    }
}

HTTP_401 = {
    "error": {
        "detail": "Admin unauthorized",
        "status": status.HTTP_401_UNAUTHORIZED
    }
}

HTTP_500 = {
    "error": {
        "detail": "Internal server error",
        "status": status.HTTP_500_INTERNAL_SERVER_ERROR
    }
}
