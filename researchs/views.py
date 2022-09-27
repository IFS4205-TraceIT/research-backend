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
    queryset = Researchdata.objects.all()
    
def getData(self, id):
    value = self.kwargs.get(id, None)
    if value == "any":
        return None
    return value

def filterData(obj, query, target):
    if obj is None or query is None:
        return obj
    return obj.filter(**{target:query})