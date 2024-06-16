from django.contrib import admin, messages
from django.db.models import Count, QuerySet
from django.urls import reverse
from urllib.parse import urlencode
from django.utils.html import format_html
from . import models


# Register your models here.
class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        
# Creating a filter for price
class PriceFilter(admin.SimpleListFilter):
    title = 'price' # Human-readable title which will be displayed in the
    parameter_name = 'price' # URL parameter

    # Returns a list of tuples (lookup value, display value) 
    def lookups(self, request, model_admin):
        return [
            ('<50', 'Cheap'),
            ('>50', 'Expensive')
        ]
    
    # Returns the filtered queryset based on the value provided in the URL
    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<50':
            return queryset.filter(unit_price__lt=50)
        elif self.value() == '>50':
            return queryset.filter(unit_price__gt=50)


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
                reverse('admin:store_product_changelist')
                + '?'
                + urlencode({
            'collection__id': str(collection.id)
        }))
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )





@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ['clear_inventory']
    list_per_page = 10
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_select_related = ['collection']
    list_filter = ['collection', 'last_update', InventoryFilter, PriceFilter]
    prepopulated_fields = {'slug': ['title']}
    search_fields = ['title']

    # list_editable = ['unit_price']

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        else:
            return 'OK'

    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(request, f'{updated_count} products were successfully updated.', messages.SUCCESS)


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'order_count']
    list_editable = ['membership']
    list_select_related = ['user']
    list_per_page = 10
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    # list_per_page = 50

    @admin.display(ordering='order_count')
    def order_count(self, customer):
        url = (
                reverse('admin:store_order_changelist')
                + '?'
                + urlencode({
            'customer__id': str(customer.id)
        })
        )
        # order_count = customer.order_set.count()
        # order_count = customer.count
        return format_html('<a href="{}">{}</a>', url, customer.order_count)

    # get_order_count.short_description = 'Number of Orders'

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            order_count=Count('order')
        )


class OrderItemInline(admin.StackedInline):
    autocomplete_fields = ['product']
    extra = 0
    model = models.OrderItem


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    autocomplete_fields = ['customer']
    list_display = ['id', 'order_time', 'customer']
    ordering = ['id']

    @admin.display(ordering='placed_at')
    def order_time(self, order):
        return order.placed_at
