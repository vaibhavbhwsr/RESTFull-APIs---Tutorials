# # T1: for Tutorial 1
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Snippet
from .serializers import SnippetSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import action

# Create your views here.


# Refactoring to use ViewSets                                              # T6
# User ViewSet
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides 'list' and 'retrieve' actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Snippet ViewSet
class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides 'list', 'create', 'retrieve', 'update',
    and 'destroy' actions.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_class = [permissions.IsAuthenticatedOrReadOnly,
                        IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# Creating an endpoint for the root of our API                             # T5
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


# This all views are defined above in most concise way
"""
# Creating an endpoint for the highlighted snippets                        # T5
class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_class = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


# UserList View                                                            # T4
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# UserDetail View                                                          # T4
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# The MOST Consisely creating API "It's really Awesome"
# Using generic class-based views illustrated in T3 django-rest-framework.org
# SnippetList View
class SnippetList(generics.ListCreateAPIView):
    permission_class = [permissions.IsAuthenticatedOrReadOnly]             # T4
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def perform_create(self, serializer):                                  # T4
        serializer.save(owner=self.request.user)


# SnippetDetail View
class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_class = [permissions.IsAuthenticatedOrReadOnly,
                        IsOwnerOrReadOnly]                                 # T4
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
"""

"""
# Using Mixins with GenericAPIView illustrated in T3 django-rest-framework.org
class SnippetList(mixins.ListModelMixin, mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        # This list() is provided by ListModelMixin
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # This create() is provided by CreateModelMixin
        return self.create(request, *args, **kwargs)


class SnippetDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        # This retrieve() is provided by RetrieveModelMixin
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        # This update() is provided by UpdateModelMixin
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # This destroy() is provided by DestroyModelMixin
        return self.destroy(request, *args, **kwargs)
"""

# This is APIView well explained in T3 of django-rest-framework.org
"""
class SnippetList(APIView):
    '''
    List all snippets, or create a new snippet.
    '''

    def get(self, request, format=None):
        snippet = Snippet.objects.all()
        serializer = SnippetSerializer(snippet, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):
    '''
    Retrieve, update or delete a snippet instance
    '''

    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status.HTTP_204_NO_CONTENT)
"""


# This is FBV of handling APIs of T1,T2 of django-rest-framework.org
"""
# format=none handle all patterns for urls containing json,xml,etc.
# @csrf_exempt                                                             # T1
@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
    '''
    List all code snippet or creating new snippet.
    '''
    if request.method == 'GET':
        snippet = Snippet.objects.all()
        serializer = SnippetSerializer(snippet, many=True)
        # return JsonResponse(serializer.data, safe=False)                 # T1
        return Response(serializer.data)

    elif request.method == 'POST':
        # data = JSONParser().parse(request)                               # T1
        # serializer = SnippetSerializer(data=data)                        # T1
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return JsonResponse(serializer.data, status=201)             # T1
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return JsonResponse(serializer.errors, status=400)               # T1
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt                                                             # T1
@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    '''
    Retrieve, Update or delete a code snippet.
    '''
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        # return JsonResponse(status=404)                                  # T1
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        # return JsonResponse(serializer.data)                             # T1
        return Response(serializer.data)

    elif request.method == 'PUT':
        # data = JSONParser().parse(request)                               # T1
        # serializer = SnippetSerializer(snippet, data=data)               # T1
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return JsonResponse(serializer.data)                         # T1
            return Response(serializer.data)
        # return JsonResponse(serializer.errors, status=400)               # T1
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        # return HttpResponse(status=204)                                  # T1
        return Response(status=status.HTTP_204_NO_CONTENT)
"""
