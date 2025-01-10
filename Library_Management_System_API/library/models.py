from django.contrib.auth.models import BaseUserManager,AbstractBaseUser, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    date_of_membership = models.DateField(auto_now_add=True)
    active_status = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
    
class Book(models.Model):
    title = models.CharField(max_length=50, null=False)
    author = models.CharField(max_length=50, null=False)
    isbn = models.CharField(max_length=50, unique=True, null=False)
    published_date = models.DateField(null=False)
    copies_available = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='transactions')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='transactions')
    borrowed_date = models.DateField(auto_now_add=True)
    returned_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"
    
    #Enforcing a database-level constraint that prevents a user from borrowing the same book multiple times without first returning it.
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'book'],
                condition=models.Q(returned_date__isnull=True),
                name='unique_active_borrow'
            )
        ]
