# apps/businesses/api/views.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class BusinessContextDebugView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "user": request.user.username,
            "business": getattr(request, "business", None) and {
                "id": request.business.id,
                "name": request.business.name,
            },
            "business_role": getattr(request, "business_role", None),
        })
