from rest_framework import viewsets
from articles.models import Article
from articles.serializers import ArticleSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    @action(detail=False, methods=['GET'])
    def by_topic(self, request):
        topic_name = request.GET.get('topic')

        if not topic_name:
            return Response({"error": "Topic parameter is required"}, status=400)

        filtered_articles = Article.objects.filter(topic=topic_name)
        serialized_data = ArticleSerializer(filtered_articles, many=True).data

        return Response(serialized_data)
