from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

# Choices for the gender field
GENDER_CHOICES = (
    ("M", "Male"),
    ("F", "Female"),
)

# Choices for the scent field
SCENT_CHOICES = (
    ("chocolate", "Chocolate scent"),
    ("nutty", "Nutty scent"),
    ("fruity", "Fruity scent"),
    ("floral", "Floral scent"),
)


class ReconiUserManager(BaseUserManager):
    def create_user(self, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError("The E-Mail field must be set")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password=password, **extra_fields)


class ReconiUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=100,
        unique=True,
    )
    nickname = models.CharField(max_length=50, unique=True, default="NickName")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    age = models.IntegerField(blank=True, null=True)
    favorite_scent = models.CharField(
        max_length=100, choices=SCENT_CHOICES, blank=True
    )
    # 향미를 나타내는 필드 (0 ~ 10 사이의 값, 기본값 0.0)
    aroma = models.FloatField(
        default=0.0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    # 단맛을 나타내는 필드 (0 ~ 10 사이의 값, 기본값 0.0)
    sweetness = models.FloatField(
        default=0.0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    # 바디감을 나타내는 필드 (0 ~ 10 사이의 값, 기본값 0.0)
    body_feel = models.FloatField(
        default=0.0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    # 산미를 나타내는 필드 (0 ~ 10 사이의 값, 기본값 0.0)
    acidity = models.FloatField(
        default=0.0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    # 로스팅 특징을 나타내는 필드 (0 ~ 10 사이의 값, 0.5 step, 기본값 0.5)
    roasting_characteristics = models.FloatField(
        default=0.5, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = ReconiUserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return str(self.nickname)

    def has_perm(self, perm, obj=None):
        return True

    def has_perms(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta(AbstractBaseUser.Meta):
        ordering = ["-date_joined"]
        db_table = "users"
