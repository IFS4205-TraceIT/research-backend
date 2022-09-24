from django.urls import path

from .views import (
    ListResearchAPIView
)

app_name = 'researchs'

urlpatterns = [
    path('researchs', ListResearchAPIView.as_view()),
    path('researchs/<input>', ListResearchAPIView.as_view())
]