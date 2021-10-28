from django.urls import path

from . import views

app_name = "employees"
urlpatterns = [
    path('', views.index, name="index"),
    path('new/', views.create, name="create"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('confirm/', views.confirm, name='confirm'),
    path('weekly_pickup/',views.weekly_pickup, name='weekly_pickup' )
    
]