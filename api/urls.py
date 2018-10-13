from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from .views import Login, YesMan, PersonViewSet

router = DefaultRouter()
router.register('persons', PersonViewSet, 'persons')

urlpatterns = [
    path('docs/', include_docs_urls(title='スキル管理システムWebAPI')),
    path('login', Login.as_view(), name='login'),
    path('yesman', YesMan.as_view()),
    path('', include(router.urls)),
]