from django.shortcuts import render
from django.db.models import Q, F
from store.models import Product, Order, Review

# Create your views here.
def home(request):
  query_set = Order.objects.select_related('customer').prefetch_related('orderitem_set').order_by('-placed_at')[:5]
  queryset = Review.objects.filter(product_id=2)
  return render(request, 'index.html', {'reviews': queryset})

# admin
# 

# def reviews(request):
#   queryset = 