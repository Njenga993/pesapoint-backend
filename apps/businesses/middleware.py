from django.http import JsonResponse
from apps.businesses.models import BusinessUser


class BusinessContextMiddleware:
    """
    Attach X-Business-ID to request ONLY.
    Authentication happens later in DRF.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # DO NOT check request.user here
        request.business = None
        request.business_role = None

        request.business_id = request.headers.get("X-Business-ID")

        return self.get_response(request)
