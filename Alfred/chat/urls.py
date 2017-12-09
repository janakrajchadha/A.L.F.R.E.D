from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^58664f9cbf53f2acb83d9c9afa9bf9011561a43c6cb4bcab4f/?$', views.AlfredView.as_view()),
]
