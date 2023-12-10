
from django.urls import path
from rest_framework.routers import SimpleRouter
from articles.views import ArticleEditorViewSet, ArticleViewSet

router = SimpleRouter()
router.register('', ArticleViewSet, basename='articles')
router.register('editor', ArticleEditorViewSet, basename='article-editors')

urlpatterns = router.urls