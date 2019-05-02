from django.urls import path

from . import views

app_name = 'datagen'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:experiment_id>/', views.experiment, name='experiment'),
]
