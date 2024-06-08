from django.db import models

# Create your models here.

from django.db import models

class Coin(models.Model):
    coin_name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)
    price_change = models.FloatField(default=0.0)
    # ... other scraped data fields

    def __str__(self):
        return self.coin_name
