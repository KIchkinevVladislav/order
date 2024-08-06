from django.contrib import admin
from admintimestamps import TimestampedAdminMixin

from .models import FoodCategory, Food


@admin.register(FoodCategory)
class FoodCategoryAdmin(admin.ModelAdmin, TimestampedAdminMixin):
    list_display = ('id', 'name_ru', 'order_id', )
    fields = ('name_ru', 'name_en', 'name_ch', 'order_id', )

    list_filter = ('order_id', )
    search_fields = ('name_ru', 'order_id', )
    ordering = ('name_ru', 'order_id', )

    timestamp_fields = ('created_at', 'modified_at')


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin, TimestampedAdminMixin):
    list_display = ('id', 'name_ru', 'description_ru', 'cost', 'category', 'is_vegan', 'is_special', 
                    'internal_code', 'is_publish', 'get_additional', )
    fields = ('name_ru', 'cost', 'category', 'is_publish', 'is_vegan', 'is_special', 
                'code', 'internal_code', ('description_ru', 'description_en', 'description_ch'),
                'additional')
    list_filter = ('category', 'is_publish', 'is_vegan', 'is_special', 'code',)
    search_fields = ('name_ru', 'code', 'internal_code', 'cost', )
    ordering = ('name_ru', 'cost', 'code', 'internal_code', )

    timestamp_fields = ('created_at', 'modified_at', )

    filter_horizontal = ('additional', )

    def get_additional(self, obj):
        return ", ".join([str(food.internal_code) for food in obj.additional.all()])
    
    get_additional.short_description = 'Дополнительные товары'
