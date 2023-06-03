from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.
class Income(models.Model):

    owner = models.ForeignKey(User, related_name="incomes", on_delete=models.SET_NULL, null=True)
    income = models.CharField(max_length=100)
    amount_of_income = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Income: {self.income}   amount of income {self.amount_of_income} from {self.created_at}"


class Outcome(models.Model):

    # user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="outcome", on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name="outcomes", on_delete=models.SET_NULL, null=True)
    outcome = models.CharField(max_length=100)
    amount_of_outcome = models.FloatField(validators=[MinValueValidator(0)])
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Outcome : {self.outcome} amount of outcome: {self.amount_of_outcome}        created at: {self.created_at:%Y-%m-%d %H:%M}"
