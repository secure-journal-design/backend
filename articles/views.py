from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from articles.models import Article
from articles.serializers import ArticleDetailSerializer, ArticleSerializer, AuthorArticleSerializer, TopicSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from articles.permissions import IsArticleEditor, IsAuthorOrReadOnly
from rest_framework.permissions import IsAuthenticated

class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly]
    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = Article.objects.all().order_by('-created_at')
        return queryset

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = ArticleDetailSerializer
        return super().retrieve(request, *args, **kwargs)

    @action(detail=False, methods=['GET'])
    def by_topic(self, request, *args, **kwargs):
        topic_name = request.GET.get('topic')

        topic_serializer = TopicSerializer(data={'topic': topic_name})
        topic_serializer.is_valid(raise_exception=True)
        topic_name = topic_serializer.validated_data['topic']
        filtered_articles = Article.objects.filter(topic=topic_name)
        serialized_data = ArticleSerializer(filtered_articles, many=True).data
        for article in serialized_data:
            article['picture_url'] = 'http://localhost:8000' + article['picture_url']
        return Response(serialized_data)

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated], authentication_classes = [TokenAuthentication, SessionAuthentication])
    def like(self, request, pk=None):
        article = self.get_object()
        user = request.user
        print(user)
        if article:
            article.likes.add(user)
            article.save()
            return Response({'detail': 'Article liked successfully.'}, status=200)

class ArticleEditorViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
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