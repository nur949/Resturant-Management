from django.db import models

class RestaurantSetting(models.Model):
    name = models.CharField(max_length=255, default='RestoManager')
    tagline = models.CharField(max_length=255, blank=True, null=True, default='Authentic Cuisine')
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    logo = models.ImageField(upload_to='settings/', blank=True, null=True)
    
    # Financial Settings
    currency_symbol = models.CharField(max_length=10, default='$')
    default_tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    trn_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Tax Registration Number")
    
    # Operational Settings
    low_stock_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=5.00)

    class Meta:
        verbose_name = "Restaurant Setting"
        verbose_name_plural = "Restaurant Settings"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Ensure only one instance exists (Singleton)
        if not self.pk and RestaurantSetting.objects.exists():
            return
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
