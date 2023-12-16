from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from articles.models import Article
from articles.serializers import ArticleDetailSerializer, ArticleSerializer, AuthorArticleSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from articles.permissions import IsArticleEditor, IsAuthorOrReadOnly
from rest_framework.permissions import IsAuthenticated

class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = ArticleDetailSerializer
        return super().retrieve(request, *args, **kwargs)

    @action(detail=False, methods=['GET'])
    def by_topic(self, request):
        topic_name = request.GET.get('topic')

        if not topic_name:
            return Response({"error": "Topic parameter is required"}, status=400)

        filtered_articles = Article.objects.filter(topic=topic_name)
        serialized_data = ArticleSerializer(filtered_articles, many=True).data

        return Response(serialized_data)
    
    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        article = self.get_object()
        user = request.user

        if article:
            article.likes.add(user)
            article.save()
            return Response({'detail': 'Article liked successfully.'}, status=200)

        return Response({'detail': 'Unable to like the article.'}, status=400)

class ArticleEditorViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsArticleEditor]
    queryset = Article.objects.all()
    serializer_class = AuthorArticleSerializer

    def list(self, request, *args, **kwargs):
        self.serializer_class = ArticleSerializer
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = ArticleDetailSerializer
        return super().retrieve(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)