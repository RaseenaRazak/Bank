from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.safestring import mark_safe

from .forms import PersonCreationForm
from .models import Person, Branch


def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        un = request.POST['username']
        pw = request.POST['password']
        cpw = request.POST['c_password']

        if pw == cpw:
            if User.objects.filter(username=un).exists():
                messages.info(request, 'username already exist')
                return redirect('register')
            else:
                user = User.objects.create_user(username=un, password=pw)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'password mismatch')

    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        un = request.POST['username']
        pw = request.POST['password']
        user = auth.authenticate(username=un, password=pw)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid user')
            # user.save()
            return redirect('login')

    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def person_create_view(request):
    form = PersonCreationForm()
    if request.method == 'POST':
        form = PersonCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, mark_safe("Application accepted. "
                                             "Click<a href='/'>Here </a> to go to home"))

            return redirect('person_add')
    return render(request, 'home.html', {'form': form})


def person_update_view(request, pk):
    person = get_object_or_404(Person, pk=pk)
    form = PersonCreationForm(instance=person)
    if request.method == 'POST':
        form = PersonCreationForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('person_change', pk=pk)
    return render(request, 'home.html', {'form': form})


# AJAX
def load_branches(request):
    district_id = request.GET.get('district_id')
    branches = Branch.objects.filter(district_id=district_id).all()
    return render(request, 'branch_dropdown_list_options.html', {'branches': branches})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)


def success(request):
    return render(request, 'success.html')
