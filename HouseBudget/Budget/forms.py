from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from Budget.models import Income, Outcome


User = get_user_model()
class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=101)
    last_name = forms.CharField(max_length=101)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class IncomeModelForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = [
            "income",
            "amount_of_income",
        ]

class OutcomeModelForm(forms.ModelForm):
    class Meta:
        model = Outcome
        fields = [
            "outcome",
            "amount_of_outcome",
        ]