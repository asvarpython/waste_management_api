from django.db import models
from django.contrib.auth import get_user_model
class Tags(models.Model):
    title = models.CharField(max_length=50)
    def __str__(self):
        return self.title


class Snippets(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True
    )
    title = models.CharField(max_length=50)
    file = models.FileField(blank=True, default='')
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tags,blank=True)

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['created']



class Products(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True
    )
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    image = models.ImageField(blank=True, default='')
    UNIT_CHOICES = (
        ('kg', 'Kilogram'),
        ('pound', 'Pound'),
    )
    unit = models.CharField(max_length=100, choices=UNIT_CHOICES)
    
    qty = models.DecimalField(
                         max_digits = 10,
                         decimal_places = 2)
    price = models.DecimalField(
                         max_digits = 10,
                         decimal_places = 2)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    class Meta:
        permissions = (
            ("manager_permission", "Manager Permission"),
        )
        ordering = ['created']
        


class Sales(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True
    )
    product = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        null=True
    )
    qty = models.DecimalField(
                         max_digits = 10,
                         decimal_places = 2,default=0.00)
    estimation_price = models.DecimalField(
                         max_digits = 10,
                         decimal_places = 2)
    created = models.DateTimeField(auto_now_add=True)

  
    class Meta:
        ordering = ['created']
    @property
    def qty_estimation_price(self):
        return None


class Pickup(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True
    )
    sale = models.ForeignKey(
        Sales,
        on_delete=models.CASCADE,
        null=True
    )
    address = models.TextField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']