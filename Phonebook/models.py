from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.conf import settings
from django.db.models import Q



class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The phone number must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def __str__(self):
        return self.name


class SpamNumber(models.Model):
    phone_number = models.CharField(max_length=15)
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reported_at = models.DateTimeField(auto_now_add=True)

    # Add a field to track if the phone number is flagged as spam
    spam_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Spam: {self.phone_number} reported by {self.reported_by.name}"

    @classmethod
    def check_and_update_spam_status(cls, phone_number):
        """
        Check if a phone number should be marked as spam based on user reports.
        If more than 5 users mark the number as spam, it is flagged as spam.
        """
        # Count the number of unique users who have reported the phone number as spam
        total_reports = cls.objects.filter(phone_number=phone_number).values('reported_by').distinct().count()

        # If more than 5 users have marked it as spam, flag it as spam
        if total_reports > 5:
            # Update the spam status for this phone number
            cls.objects.filter(phone_number=phone_number).update(spam_status=True)
            return True

        return False

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)