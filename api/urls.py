from django.urls import path

from .views import FoodListView

app_name = 'api'


urlpatterns = [
    path('foods/', FoodListView.as_view(), name='foods'),
]
