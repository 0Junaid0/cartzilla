from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image

class User(AbstractUser):
    """
    Custom User model for Cartzilla.
    """

    class Roles(models.TextChoices):
        CUSTOMER = 'customer', _('Customer')
        SELLER = 'seller', _('Seller')

    role = models.CharField(max_length=10, choices=Roles.choices, default=Roles.CUSTOMER)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    is_verified_seller = models.BooleanField(default=False)  # For seller verification

    def is_seller(self) -> bool:
        return self.role == User.Roles.SELLER

    def is_customer(self) -> bool:
        return self.role == User.Roles.CUSTOMER

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Resize Profile Picture
        if self.profile_picture:
            img = Image.open(self.profile_picture.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.profile_picture.path)

    def __str__(self):
        return self.username
