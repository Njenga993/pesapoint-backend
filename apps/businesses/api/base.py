from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from apps.businesses.models import BusinessUser


class BusinessScopedViewSet(ModelViewSet):
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        business_id = request.headers.get("X-Business-ID")
        if not business_id:
            raise PermissionDenied("Business context missing")

        try:
            membership = BusinessUser.objects.select_related("business").get(
                user=request.user,
                business_id=business_id,
                is_active=True,
            )
        except BusinessUser.DoesNotExist:
            raise PermissionDenied("Not a member of this business")

        request.business = membership.business
        request.business_role = membership.role.lower()
