
from django.urls import path
from rest_framework.routers import SimpleRouter
from articles.views import ArticleViewSet

router = SimpleRouter()
router.register('', ArticleViewSet, basename='articles')

urlpatterns = router.urls