from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import truncatechars

from random import randint


class User(AbstractUser):
    # WARNING!
    """
    This model represents the User instance of the system, login system and
    everything that relates with an `User` is represented by this model.
    """

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, null=True, max_length=255)
    email = models.EmailField(unique=True)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


def get_verification_code():
    return randint(1000, 9999)


class VerificationCode(models.Model):
    user = models.OneToOneField(User, related_name="verification_code", on_delete=models.CASCADE)
    code = models.CharField(max_length=6, db_index=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))


    def __str__(self):
        return str(self.code)


    @staticmethod
    def generate_code_for_user(user):
        if hasattr(user, "verification_code"):
            obj = user.verification_code
            obj.code = get_verification_code()
            obj.is_used = False
            obj.save()
            return obj.code
        else:
            obj = VerificationCode.objects.create(
                user=user, code=get_verification_code(), is_used=False)
            return obj.code


class Feedback(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='feedback')
    description = models.TextField(_('Description'))
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Feedback')
        verbose_name_plural = _('Feedbacks')
        ordering = ['-id']

    def __str__(self):
        return '%s' % self.description

    @property
    def short_description(self):
        return truncatechars(self.description, 40)