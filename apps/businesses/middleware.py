from django.http import JsonResponse
from apps.businesses.models import Business, BusinessUser


class BusinessContextMiddleware:
    """
    Injects request.business and request.business_role
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip unauthenticated requests
        if not request.user.is_authenticated:
            request.business = None
            request.business_role = None
            return self.get_response(request)

        business_id = request.headers.get("X-Business-ID")

        if not business_id:
            request.business = None
            request.business_role = None
            return self.get_response(request)

        try:
            membership = BusinessUser.objects.select_related(
                "business"
            ).get(
                user=request.user,
                business_id=business_id,
                is_active=True,
            )
        except BusinessUser.DoesNotExist:
            return JsonResponse(
                {"detail": "Invalid business context."},
                status=403,
            )

        request.business = membership.business
        request.business_role = membership.role

        return self.get_response(request)
