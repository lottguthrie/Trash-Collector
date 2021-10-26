from django.urls import path

from . import views

app_name = "employees"
urlpatterns = [
    path('', views.index, name="index"),
    path('new/', views.create, name="create"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('delete/', views.delete, name='delete'),
    path('<int:customer_id>', views.detail, name="detail"),
    path('edit/', views.edit, name='edit'),
    
]