from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .views import UserCreate

urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/register", UserCreate.as_view(), name="Register"),
    path("account/auth", obtain_auth_token, name="Authenticate"),
    path("api/board", include("board.urls")),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]