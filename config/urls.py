"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from apps.businesses.api.views import BusinessContextDebugView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from config.schema import ProtectedSchemaView


urlpatterns = [
    path('api/v1/schema/', ProtectedSchemaView.as_view() , name='api-schema'),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('api/v1/sales/', include('apps.sales.api.urls')),
    path('api/v1/receipts/', include('apps.receipts.api.urls')),
    path('api/v1/accounts/', include('apps.accounts.api.urls')),
    path('api/v1/businesses/', include('apps.businesses.api.urls')),
    path('api/v1/products/', include('apps.products.api.urls')),
    path("debug-context/", BusinessContextDebugView.as_view()),
]
