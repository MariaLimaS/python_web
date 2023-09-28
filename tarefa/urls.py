from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import TarefaView

urlpatterns = [
    
    path("", TarefaView.as_view()),
    path("<id>/", TarefaView.as_view()),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)