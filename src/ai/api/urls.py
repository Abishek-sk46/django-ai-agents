from django.urls import path

from ai.api.views import AgentQueryAPIView


urlpatterns = [
    path("agent/query", AgentQueryAPIView.as_view(), name="agent-query"),
]