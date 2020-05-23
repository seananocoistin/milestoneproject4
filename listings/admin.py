from django.contrib import admin
from .models import Listing, Category

# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = (
        'contact_details',
        'business_name',
        'category',
        'rating',
        'image',
        'business_hours',
        'description',
        'is_premium',
    )

   # ordering = ('',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )

admin.site.register(Listing, ListingAdmin)
admin.site.register(Category, CategoryAdmin)