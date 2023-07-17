import logging


class LogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger = logging.getLogger("user_logs")
        user = request.user
        method = request.method
        url = request.path
        logger.info(
            "User %s accessed URL: %s using method: %s.",
            user.username,
            url,
            method,
        )

        response = self.get_response(request)

        return response
