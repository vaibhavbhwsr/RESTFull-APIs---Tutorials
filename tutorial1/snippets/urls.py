# from rest_framework.urlpatterns import format_suffix_patterns
# from .views import SnippetViewSet, UserViewSet
# from rest_framework import renderers
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


# T6 This is the most concise code for URLConfigs for APIViews.

# Create a router and register our viewset with it
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

# The api URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]


# Binding ViewSets to URLs explicitly                                      # T6
"""
snippet_list = SnippetViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
snippet_detail = SnippetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delet': 'destroy'
})
snippet_highlight = SnippetViewSet.as_view({
    'get': 'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])
user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})


urlpatterns = format_suffix_patterns([
    path('', views.api_root),
    path('snippets/', snippet_list, name='snippet-list'),
    path('snippets/<int:pk>/', snippet_detail, name='snippet-detail'),
    path('snippets/<int:pk>/highlight/', snippet_highlight,
         name='snippet-highlight'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail')
])
"""

# Before T5
"""
urlpatterns = [
    # CBV
    path('', views.api_root),
    path('snippets/<int:pk>/highlight/', views.SnippetHighlight.as_view(),
         name='snippet-highlight'),

    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>', views.UserDetail.as_view(), name='user-detail'),

    path('snippets/', views.SnippetList.as_view(), name='snippet-list'),
    path('snippets/<int:pk>', views.SnippetDetail.as_view(),
         name='snippet-detail'),

    # FBV
    # path('snippets/', views.snippet_list),
    # path('snippets/<int:pk>', views.snippet_detail),
]
"""

"""
We don't necessarily need to add these extra url patterns in, but it gives us a
simple, clean way of referring to a specific format.
"""
"""
urlpatterns = format_suffix_patterns(urlpatterns)
"""
