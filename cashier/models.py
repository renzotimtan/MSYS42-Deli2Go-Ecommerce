from django.db import models

# Create your models here.
class Item(models.Model):
    CATEGORY = (
        ("Alcohol and Hygiene", "Alcohol and Hygiene"),
        ("Candy/Gum", "Candy/Gum"),
        ("Canned Drinks/Bottled Drinks/Powdered Drinks", "Canned Drinks/Bottled Drinks/Powdered Drinks"),
        ("Gong Cha", "Gong Cha"),
        ("Magazines", "Magazines"),
        ("Pastries", "Pastries"),
        ("Potato Corner", "Potato Corner"),
        ("Snacks", "Snacks"),
        ("Turks", "Turks")
    )

    image = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=500, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY)
    brand = models.CharField(max_length=50)
    stock = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name





