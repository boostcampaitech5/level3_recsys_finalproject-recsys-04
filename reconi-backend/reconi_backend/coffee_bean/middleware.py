import logging
from django.contrib.auth.models import AnonymousUser


class LogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger = logging.getLogger("user_logs")
        user = request.user
        method = request.method
        url = request.path

        if isinstance(user, AnonymousUser):
            nickname = "AnonymousUser"
        else:
            nickname = user.nickname
        logger.info(
            "User %s accessed URL: %s using method: %s.",
            nickname,
            url,
            method,
        )

        response = self.get_response(request)

        return response
