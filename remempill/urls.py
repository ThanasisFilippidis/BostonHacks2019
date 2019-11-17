from django.contrib import admin
from django.urls import path

from remempill import views
from remempill.views import *


urlpatterns = [
    # path('', views.index, name='index'),
    path('', Index.as_view(), name="index"),
    path('pillcase/<str:elder_id>', Pillcase.as_view(), name="pillcase"),
    path('mylogout/', views.mylogout, name="mylogout"),
    path('callresponse/<str:consumption_id>', views.callresponse, name="callresponse"),
    path('dynamic_call_creator/<str:consumption_id>', views.dynamic_call_creator, name="dynamic_call_creator"),
]

admin.site.site_header = 'RememPill Administration Site'
admin.site.site_title = 'RememPill Administration Site'
