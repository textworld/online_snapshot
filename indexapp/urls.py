from django.urls import path
from . import views

app_name = 'indexapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('list', views.PageListView.as_view(), name='list'),
    path('<int:page_id>/', views.detail, name='detail')
]
