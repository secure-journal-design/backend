
from django.urls import path
from rest_framework.routers import SimpleRouter
from articles.views import ArticleEditorViewSet, ArticleViewSet

router = SimpleRouter()
router.register(r'editor', ArticleEditorViewSet, basename='article-editors')
router.register(r'', ArticleViewSet, basename='articles')

urlpatterns = router.urls