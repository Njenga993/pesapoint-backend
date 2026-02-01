from rest_framework.schemas.views import SchemaView
from rest_framework.schemas.openapi import SchemaGenerator
from rest_framework.permissions import IsAuthenticated

class ProtectedSchemaView(SchemaView):
    permission_classes = [IsAuthenticated]
    schema_generator_class = SchemaGenerator
    
