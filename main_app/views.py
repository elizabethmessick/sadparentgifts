from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Gift
from django.views.generic.edit import CreateView, UpdateView, DeleteView


# Create your views here.


def discover_gifts(request):
    gifts = Gift.objects.all()
    return render(request, 'discover_gifts.html', {'gifts': gifts})

# implement photo_url
# google how to change from all to 10 random list items


def about(request):
    return render(request, 'about.html')


def profile(request, id):
    profile = User.objects.get(id=id)
    return render(request, 'profile.html', {'profile': profile})


def gifts_detail(request, gift_id):
    gift = Gift.objects.get(id=gift_id)
    return render(request, 'gifts/detail.html', {'gift': gift})


# Authentication views


def login_view(request):
    if request.method == 'POST':
        # if post, then authenticate (user submitted username and password)
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username=u, password=p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    print("The account has been disabled.")
                    return HttpResponseRedirect('/')
            else:
                print("The username and/or password is incorrect.")
                return HttpResponseRedirect('/')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('discover_gifts')
        else:
            return redirect('/signup/')
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})


# CRUD views


class GiftCreate(CreateView):
    model = Gift
    fields = ['description', 'photo_url']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect('/')


class GiftUpdate(UpdateView):
    model = Gift
    fields = ['description', 'photo_url']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect('/' + str(self.object.pk))


class GiftDelete(DeleteView):
    model = Gift
    success_url = '/'
