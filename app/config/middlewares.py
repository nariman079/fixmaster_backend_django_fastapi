import time
from config import csm_metrics

class RequestTimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        duration = time.time() - start_time

        # Определяем view (если возможно)
        view_name = getattr(request.resolver_match, 'url_name', 'unknown')
        method = request.method
        status = response.status_code

        csm_metrics.APP_REQUEST_DURATION.labels(
            method=method,
            view=view_name,
            status=status
        ).observe(duration)

        return response