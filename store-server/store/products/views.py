from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
#from django.core.cache import cache

from products.models import Product, ProductCategory, Basket
from common.views import TitleMixin
# Create your views here.


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'


#def index(request):
#    context = {'title': 'Store'}
#    return render(request, 'products/index.html', context=context)


class ProductsListView(TitleMixin, ListView):
    model = Product
    paginate_by = 3
    template_name = 'products/products.html'
    title = 'Store - Каталог'
    ordering = ('id',)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        # categories = cache.get('categories')
        # if not categories:
        #     context['categories'] = ProductCategory.objects.all()
        #     cache.set('categories', context['categories'], 30)
        # else:
        #     context['categories'] = categories
        context['categories'] = ProductCategory.objects.all()
        return context
    
    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset


#def products(request, category_id=None, page_number=1):
#    products = Product.objects.filter(category__id=category_id) if category_id else Product.objects.all()
#    
#    per_page = 3
#    paginator = Paginator(products, per_page=per_page)
#    products_paginator = paginator.page(page_number)
#
#    context = {'title': 'Store - Каталог',
#               'products': products_paginator,
#               'categories': ProductCategory.objects.all(),
#    }
#
#    return render(request, 'products/products.html', context=context)


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()

    return HttpResponseRedirect(request.META['HTTP_REFERER']) 
