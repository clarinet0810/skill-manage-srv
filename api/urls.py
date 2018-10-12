from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Login, YesMan, PersonViewSet

router = DefaultRouter()
router.register(r'persons', PersonViewSet, r'persons')

urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('yesman', YesMan.as_view()),
    path('', include(router.urls)),
]