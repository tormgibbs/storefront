from django.urls import path, include
from . import views
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register(r'products', views.ProductsViewSet, 'product')
router.register(r'collections', views.CollectionViewSet, 'collection')
router.register(r'carts', views.CartViewSet, 'cart')
router.register(r'customers', views.CustomerViewSet, 'customer')
router.register(r'orders', views.OrderViewSet, 'order')


products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register(r'reviews', views.ReviewViewSet, 'product-reviews')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register(r'items', views.CartItemViewSet, 'cart-items')


store_api = router.urls + products_router.urls + carts_router.urls


urlpatterns = [
    path('api/', include(store_api)),
]