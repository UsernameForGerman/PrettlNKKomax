from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

from komax_app.models import Komax
from .serializers import *


# Entry point(temporary)
#TODO: rewrite entry point
def index(request):
    return render(request, 'komax_app/index.html', context={"name" : "a"})

class EquipmentListView(APIView):
    """
    View to list all equipment

    * Requires token authentication.
    * All are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    def get_object(self, number):
        try:
            return Komax.objects.get(number=number)
        except Komax.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        komaxes = Komax.objects.all()
        komax_serializer = KomaxSerializer(komaxes, context={'request': request}, many=True)

        return Response(komax_serializer.data)

    def post(self, request, *args, **kwargs):
        komax_serializer = KomaxSerializer(data=request.data)
        if komax_serializer.is_valid():
            komax_serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(komax_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, number, *args, **kwargs):
        komax = self.get_object(number)
        if komax is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        komax_serializer = KomaxSerializer(komax, data=request.data, context={'request': request})
        if komax.is_valid():
            komax.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(komax_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, number, *args, **kwargs):
        komax = self.get_object(number)
        if komax is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        komax.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""
@api_view(['GET', 'POST'])
def komax_list(request):
    if request.method == 'GET':
        data = Komax.objects.all()

        serializer = KomaxSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = KomaxSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def komax_detail(request, pk):
    try:
        student = Komax.objects.get(pk=pk)
    except Komax.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = KomaxSerializer(student, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""
