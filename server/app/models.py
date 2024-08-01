from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.hashers import make_password
from django.db import models

class Organization(models.Model):
    name = models.CharField(max_length=100)

class Database(models.Model):
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE, primary_key=True)
    host = models.CharField(max_length=250)
    port = models.CharField(max_length=5)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=250)
    database_schema = models.CharField(max_length=250)

    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)  # Hash the password before saving
        super().save(*args, **kwargs)

class User(AbstractUser):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    is_admin = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  
        blank=True,
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.pk and not self.organization:
            organization = Organization.objects.create(name=self.username + "'s organization")
            self.organization = organization
            self.is_admin = True
        super().save(*args, **kwargs)
    
    