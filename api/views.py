from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .models import FoodCategory, Food
from .serializers import FoodListSerializer, FoodSerializer


class FoodListView(ListAPIView):
    serializer_class = FoodListSerializer

    def get_queryset(self):
        return FoodCategory.objects.filter(food__is_publish=True).distinct().order_by('id')


    def list(self, request, *args, **kwargs):
        published_foods = Food.objects.filter(is_publish=True)
        
        categories = self.get_queryset()
        category_ids = categories.values_list('id', flat=True)
        
        filtered_foods = published_foods.filter(category__id__in=category_ids)
        
        serializer = self.get_serializer(categories, many=True)
        response_data = serializer.data

        for category_data in response_data:
            category_id = category_data['id']
            category_foods = filtered_foods.filter(category_id=category_id)
            category_data['foods'] = FoodSerializer(category_foods, many=True).data

        return Response(response_data)
