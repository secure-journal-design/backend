from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

API_TITLE = "Secure Journal Design"
API_DESCRIPTION = "API for Secure Journal"

urlpatterns = [
    path('admin-335DaqSURVyQ/', admin.site.urls),
    path('docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION)),
    path('schema/', get_schema_view(title=API_TITLE)),
]