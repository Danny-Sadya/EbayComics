from django.contrib import admin
from django.urls import path, include
from .views import GenerateGoCollectDataView

urlpatterns = [
    path('generate_goocollect_data/', GenerateGoCollectDataView.as_view(), name='generate_gocollect_data'),
]
