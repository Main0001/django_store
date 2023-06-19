from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

# Create your views here.
class OrderCreateView(TemplateView):
    template_name = 'orders/order-create.html'
