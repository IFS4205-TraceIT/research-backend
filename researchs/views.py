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
    permission_classes = (IsAuthenticated,)
    serializer_class = ResearchdataSerializer
    queryset = Researchdata.objects.all()
