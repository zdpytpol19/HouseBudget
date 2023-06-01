from django.http import HttpRequest, HttpResponse,HttpResponseBadRequest
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm
from Budget.forms import IncomeModelForm,OutcomeModelForm
from Budget.models import Income,Outcome
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

# Create your views here.
def main_page(request: HttpRequest) -> HttpResponse:
    return render(request, "main_page.html")

def home(request):
    return render(request, 'users/main_page.html')

def home_1(request):
    return render(request, 'users/main_page_1.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, f'Your account has been created. You can log in now!')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    context = {'form': form}
    return render(request, 'users/register.html', context)


class IncomeAddView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = IncomeModelForm()
        # if form is valid
        context = {"form": form}

        return render(request, "add_income_cbv.html", context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = IncomeModelForm(request.POST)
        income = form.save(commit=False)
        income.owner = request.user
        income.save()
        context = {"form": form, "income": income}

        return render(request, "add_income_cbv.html", context=context)

class OutcomeAddView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = OutcomeModelForm()
        # if form is valid
        context = {"form": form}

        return render(request, "add_outcome_cbv.html", context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = OutcomeModelForm(request.POST)
        outcome = form.save(commit=False)
        outcome.owner = request.user
        outcome.save()
        context = {"form": form, "outcome": outcome}

        return render(request, "add_outcome_cbv.html", context=context)

class IncomeListView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        # if not request.user.is_authenticated:
        #     return redirect("admin:login")
        incomes = Income.objects.filter(owner=request.user)
        context = {"incomes": incomes}

        return render(request, "income_list.html", context=context)

class OutcomeListView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        # if not request.user.is_authenticated:
        #     return redirect("admin:login")
        outcomes = Outcome.objects.filter(owner=request.user)
        context = {"outcomes": outcomes}

        return render(request, "outcome_list.html", context=context)

class IncomeDeletelView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, id: int) -> HttpResponse:
        try:
            income = Income.objects.get(
                id=id, owner=request.user
            )
        except Income.DoesNotExist:
            return HttpResponseBadRequest("Site does not exists")
        income.delete()

        return redirect("income_list.html")