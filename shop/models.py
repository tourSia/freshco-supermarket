from django.db import models
from django.urls import reverse  # Used to generate URLs by reversing the URL pat-terns
import uuid  # Required for unique book instances


class Category(models.Model):
    """Model representing a product category."""
    name = models.CharField(max_length=200, help_text='Enter a product category.')

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Product(models.Model):
    """Model representing a product."""
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=600)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Foreign Key used because product can only have one category, but category can have multiple products
    category = models.ForeignKey('Category', on_delete=models.RESTRICT, null=True)

    @property
    def average_rating(self):
        reviews = Review.objects.filter(product=self)
        if reviews.count() > 0:
            return sum([review.stars for review in reviews]) / reviews.count()
        else:
            return 0

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        """Returns the URL to access a particular product instance."""
        return reverse('product_detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.name}'


class Review(models.Model):
    """Model representing a review."""
    stars = models.IntegerField()
    text = models.CharField(max_length=1000, help_text='Please enter your thoughts')

    # Foreign Key used because review can only have one product, but product can have multiple reviews
    product = models.ForeignKey('Product', on_delete=models.RESTRICT, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.stars} {self.text}'

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this review."""
        return reverse('review_detail', args=[str(self.id)])

class Order(models.Model):
    """Model representing a specific copy of an order."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular order')

    # ManyToManyField used because orders can contain many products. Prod-ucts can be in many orders.
    products = models.ManyToManyField(Product)
    placed = models.DateField("Date", auto_now_add=True)  # captures cur-rent date

    @property
    def total(self):
        """Returns the total price of the products in the order."""
        return sum([product.price for product in self.products.all()])

    ORDER_STATUS = (
        ('p', 'preparing'), ('o', 'out for delivery'), ('r', 'received'), ('d', 'delayed'), ('c', 'cancelled'),
    )

    status = models.CharField(
        max_length=1,
        choices=ORDER_STATUS,
        blank=True,
        default='p',
        help_text='Order Status',
    )

    class Meta:
        ordering = ['placed']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.placed})'
