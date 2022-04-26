"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from api import views


urlpatterns = [
    path('api/v<int:db_id>/<slug:resource_name>',
         csrf_exempt(views.ApiResource.as_view()), name='resource'),
    path('api/v<int:db_id>/<slug:resource_name>/<int:pk>',
         csrf_exempt(views.ApiResourceItem.as_view()), name='resource_item'),
    path('api/v<int:db_id>/<slug:resource_name>/<int:pk>/<slug:subresource_name>',
         csrf_exempt(views.ApiSubResource.as_view()), name='subresource'),
    path('api/v<int:db_id>/<slug:resource_name>/<int:pk>/<slug:subresource_name>/<int:sub_pk>',
         csrf_exempt(views.ApiSubResourceItem.as_view()), name='subresource_item'),
]
