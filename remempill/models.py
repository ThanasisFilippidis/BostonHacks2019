from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            # creation_date=creation_date,
            username=username,
            # premium_ending_date=premium_ending_date,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            email,
            password=password,
            # creation_date=creation_date,
            # premium_ending_date=premium_ending_date,
            # is_premium=True,
            # list_of_tracks="",
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class CareTaker(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    # creation_date = models.DateField()
    username = models.CharField(blank=True, null=True, max_length=150)
    creation_date = models.DateTimeField(editable=False, default=timezone.now)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def get_id(self):
        return self.id

    def get_elders(self):
        return GrandParent.objects.filter(care_taker=self)

    # def update_total_playlists(self, number):
    #     self.total_inserted_playlists_number = number
    #     self.save(update_fields=["total_inserted_playlists_number"])
    #
    # def get_total_tracks(self):
    #     return self.total_inserted_tracks_number


class GrandParent(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    phone = models.CharField(max_length=17, blank=True, default="")
    greeting_message = models.CharField(max_length=256, default="")

    care_taker = models.ForeignKey(CareTaker, on_delete=models.CASCADE, related_name='grandparent')

    def __str__(self):
        return self.name + " " + self.surname

    def get_pills(self):
        return Pill.objects.filter(owner=self)

    def get_n_days_pills(self, day):
        n_days_pills = []
        for tmpPill in self.get_pills():
            n_days_pills += PillConsumption.objects.filter(pill=tmpPill, time_to_consume__day=day)
        return n_days_pills

    def get_n_days_n_hours_pills(self, day, hour):
        n_days_n_hours_pills = []
        for tmpPill in self.get_pills():
            n_days_n_hours_pills += PillConsumption.objects.filter(pill=tmpPill, time_to_consume__day=day,
                                                                   time_to_consume__hour=hour)
        return n_days_n_hours_pills


class Pill(models.Model):
    name = models.CharField(max_length=30)
    shape = models.CharField(max_length=15)
    color = models.CharField(max_length=15)
    size = models.CharField(max_length=10)
    remaining = models.IntegerField()

    owner = models.ForeignKey(GrandParent, on_delete=models.CASCADE, related_name="pill")

    def __str__(self):
        return str(self.owner) + "'s " + self.name


class PillConsumption(models.Model):
    pill = models.ForeignKey(Pill, on_delete=models.CASCADE, related_name="pill_consumption")
    time_to_consume = models.DateTimeField(null=True, blank=True)
    consumed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pill) + " " + str(self.time_to_consume)

    def set_consumed(self):
        self.consumed = True
        self.save(update_fields=["consumed"])
