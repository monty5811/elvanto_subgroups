# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from elvanto_subgroups.models import ElvantoPerson
from elvanto_subgroups.serializers import ElvantoPersonSerializer


class ApiCollection(APIView):
    permission_classes = (IsAuthenticated,)
    model_class = None
    serializer_class = None

    def get(self, request, format=None):
        objs = self.model_class.objects.all()
        serializer = self.serializer_class(objs, many=True)
        return Response(serializer.data)


class ApiMember(APIView):
    permission_classes = (IsAuthenticated,)
    model_class = None
    serializer_class = None

    def get(self, request, format=None, **kwargs):
        obj = get_object_or_404(self.model_class, pk=kwargs['pk'])
        serializer = self.serializer_class(obj)
        return Response(serializer.data)
