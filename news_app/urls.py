from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user import views
from django.contrib import admin

router = DefaultRouter()
router.register(r'user', views.UserViewSet)

urlpatterns = [
    path('admin', admin.site.urls),
    path('', include(router.urls)),
]
