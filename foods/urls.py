from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='foods.index'),
    path('<int:id>/', views.show, name='foods.show'),
    path('<int:id>/review/create/', views.create_review, name='foods.create_review'),
    path('<int:id>/review/<int:review_id>/edit/', views.edit_review, name='foods.edit_review'),
    path('<int:id>/review/<int:review_id>/delete/', views.delete_review, name='foods.delete_review'),
]