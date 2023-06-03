from django.contrib.auth.decorators import login_required
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
        #if form is valid:
        context = {"form": form}

        return render(request, "add_outcome_cbv.html", context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = OutcomeModelForm(request.POST)
        outcome = form.save(commit=False)
        outcome.owner = request.user
        outcome.save()
        context = {"form": form, "outcome": outcome }

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

@login_required
def income_delete(request: HttpRequest, id: int) -> HttpResponse:
    """
    Widok do usuwania samochodu, najpierw pobieramy obiekt dla danego id i aktualnie zalogowanego użytkownika,
    następnie usuwamy, jeśli żadnego obiektu nie wyciągniemy z bazy to po prostu nic się nie usunie
    """
    try:
        income = Income.objects.get(id=id, owner=request.user)  # Upewniam się tutaj, że samochód należy do zalogowanego usera
        # Jeśli nie to nie zostanie odnaleziony w bazie
    except Income.DoesNotExist:
        return HttpResponseBadRequest("Site does not exists")
    income.delete()

    return redirect("income_list")  # Tutaj podaję name urla na który ma mnie przekierować

@login_required
def outcome_delete(request: HttpRequest, id: int) -> HttpResponse:
    """
    Widok do usuwania samochodu, najpierw pobieramy obiekt dla danego id i aktualnie zalogowanego użytkownika,
    następnie usuwamy, jeśli żadnego obiektu nie wyciągniemy z bazy to po prostu nic się nie usunie
    """
    try:
        outcome = Outcome.objects.get(id=id, owner=request.user)  # Upewniam się tutaj, że samochód należy do zalogowanego usera
        # Jeśli nie to nie zostanie odnaleziony w bazie
    except Outcome.DoesNotExist:
        return HttpResponseBadRequest("Site does not exists")
    outcome.delete()

    return redirect("outcome_list")  # Tutaj podaję name urla na który ma mnie przekierować

@login_required()
def income_update(request: HttpRequest, id: int) -> HttpResponse:
    """
    Widok do edycji samochodu, tak jak dla wcześniejszych widoków upewniamy się, że obiekt istnieje w bazie danych i
    należy do aktualnie zalogowanego użytkownika. W tym widoku będzie się wyświetlał formularz z aktualnymi danymi obiektu
    możemy coś podmienić i wysłać zapytanie POST tak jak przy tworzeniu.
    """
    user = request.user  # aktualnie zalogowany użytkownik
    try:
        income = Income.objects.get(id=id, owner=request.user)  # Upewniam się tutaj, że samochód należy do zalogowanego usera
        # Jeśli nie to nie zostanie odnaleziony w bazie

        # Tu chcemy stworzyć słownik z aktualnymi danymi obiektu
        initial_data = dict(
            income=income.income,
            amount_of_income=income.amount_of_income,

        )
    except Income.DoesNotExist:
        return HttpResponseBadRequest("Site does not exists")

    if request.method == "GET":
        form = IncomeModelForm(initial=initial_data)
        context = {"form": form, "income": income}
        return render(request, "income_update.html", context=context)

    elif request.method == "POST":
        form = IncomeModelForm(request.POST)

        if form.is_valid():
            Income.objects.filter(id=id, owner=user).update(
                **form.cleaned_data
            )

            context = {"form": form, "income": income}
            messages.success(request, "Income has been successfully updated")
            return render(request, "income_update.html", context=context)
        return HttpResponseBadRequest("There are some errors in form")

@login_required()
def outcome_update(request: HttpRequest, id: int) -> HttpResponse:
    """
    Widok do edycji samochodu, tak jak dla wcześniejszych widoków upewniamy się, że obiekt istnieje w bazie danych i
    należy do aktualnie zalogowanego użytkownika. W tym widoku będzie się wyświetlał formularz z aktualnymi danymi obiektu
    możemy coś podmienić i wysłać zapytanie POST tak jak przy tworzeniu.
    """
    user = request.user  # aktualnie zalogowany użytkownik
    try:
        outcome = Outcome.objects.get(id=id, owner=request.user)  # Upewniam się tutaj, że samochód należy do zalogowanego usera
        # Jeśli nie to nie zostanie odnaleziony w bazie

        # Tu chcemy stworzyć słownik z aktualnymi danymi obiektu
        initial_data = dict(
            outcome=outcome.outcome,
            amount_of_outcome=outcome.amount_of_outcome,

        )
    except Outcome.DoesNotExist:
        return HttpResponseBadRequest("Site does not exists")

    if request.method == "GET":
        form = OutcomeModelForm(initial=initial_data)
        context = {"form": form, "outcome": outcome}
        return render(request, "outcome_update.html", context=context)

    elif request.method == "POST":
        form = OutcomeModelForm(request.POST)

        if form.is_valid():
            Outcome.objects.filter(id=id, owner=user).update(
                **form.cleaned_data
            )

            context = {"form": form, "outcome": outcome}
            messages.success(request, "Outcome has been successfully updated")
            return render(request, "outcome_update.html", context=context)

        return HttpResponseBadRequest("There are some errors in form")
