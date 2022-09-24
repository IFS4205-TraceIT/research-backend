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

    def get_queryset(self):
        queryset = Researchdata.objects.all()
        genderQuery = getData(self, "gender")
        vaccinesQuery = getData(self, "vaccines")
        print(genderQuery, vaccinesQuery)
        if genderQuery is None and vaccinesQuery is None:
            return queryset
        queryset = filterData(queryset, genderQuery, "gender")
        queryset = filterData(queryset, vaccinesQuery, "list_of_vaccines__icontains")
        return queryset
    
def getData(self, id):
    value = self.kwargs.get(id, None)
    if value == "any":
        return None
    return value

def filterData(obj, query, target):
    if obj is None or query is None:
        return obj
    return obj.filter(**{target:query})