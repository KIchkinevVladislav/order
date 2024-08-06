import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import FoodCategory, Food


class FoodListViewTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()

        cls.beverages = FoodCategory.objects.create(
            name_ru='Напитки',
            order_id=10
        )

        cls.bakery = FoodCategory.objects.create(
            name_ru='Выпечка',
            order_id=20
        )

        cls.salads = FoodCategory.objects.create(
            name_ru='Салаты',
            order_id=30
        )

        cls.product_1 = Food.objects.create(
            category=cls.beverages,
            code=1,
            internal_code=100,
            name_ru='Лимонад',
            cost=125.00,
            is_publish=True
        )

        cls.product_2 = Food.objects.create(
            category=cls.bakery,
            code=2,
            internal_code=200,
            name_ru='Круссан',
            cost=250.00,
            is_publish=True
        )        

        cls.product_3 = Food.objects.create(
            category=cls.bakery,
            code=3,
            internal_code=300,
            name_ru='Кекс',
            cost=200.00,
            is_publish=False
        ) 


    def test_get_list_foods(self):
        url = reverse('api:foods')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['id'], 1)
        self.assertEqual(len(data[1]['foods']), 1)


    def test_get_list_foods_sorted_reverse_id(self):
        url = reverse('api:foods')
        response = self.client.get(url, {'sort_by': '-id'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['id'], 2)

    def test_get_list_foods_sorted_name_ru(self):
        url = reverse('api:foods')
        response = self.client.get(url, {'sort_by': 'name_ru'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name_ru'], 'Выпечка')
