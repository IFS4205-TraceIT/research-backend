from django.shortcuts import render
from .models import Researchers, Researchdata

from .serializers import (
    ResearchdataSerializer
)

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated


class ListResearchAPIView(ListAPIView):
    serializer_class = ResearchdataSerializer
    lookup_url_kwarg = "input"

    def get_queryset(self):
        queryset = Researchdata.objects.all()
        query = self.kwargs.get(self.lookup_url_kwarg, None)
        if query is None:
            return queryset
        queryset = queryset.filter(list_of_vaccines__icontains=query)
        return queryset