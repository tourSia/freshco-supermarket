from .models import Category, Product, Review, Order
from django.shortcuts import render
from django.views import generic

def index(request):
    """View function for home page of site."""
    num_products = Product.objects.all().count()
    num_reviews = Review.objects.all().count()

    context = {
        'num_products': num_products,
        'num_reviews': num_reviews,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class ProductListView(generic.ListView):
    model = Product

class ProductDetailView(generic.DetailView):
    model = Product
