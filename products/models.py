from django.db import models


class Product(models.Model):
    
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    product_type = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    year_of_manufacture = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField(default=0)
    image = models.ImageField(upload_to='products/', default='default.png', blank=True)  # Add image field
    



    def __str__(self):
        return self.name
    
    def update_rating(self):
        """Update the product's rating based on associated reviews."""
        from users.models import Reviews  # Lazy import to avoid circular import error
        reviews = Reviews.objects.filter(product=self)
        if reviews.exists():
            total_rating = sum([review.rating for review in reviews])
            self.rating = total_rating / len(reviews)  # Calculate average rating
            self.save()  # Save the updated rating

       