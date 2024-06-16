from django.dispatch import receiver
from store.signals import order_created

@receiver(order_created)
def on_order_created(sender, **kwargs):
  # order_created.send_robust(sender, order=order)
  print(kwargs['order'])