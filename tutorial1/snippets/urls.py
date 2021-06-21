from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


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
We don't necessarily need to add these extra url patterns in, but it gives us a
simple, clean way of referring to a specific format.
"""
urlpatterns = format_suffix_patterns(urlpatterns)
