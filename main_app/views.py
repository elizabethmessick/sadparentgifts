from django.shortcuts import render, redirect
from .forms import LoginForm, CommentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Gift, Comment
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import uuid
import boto3

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'sadgiftuser'

# Create your views here.


def discover_gifts(request):
    gifts = Gift.objects.all().order_by('?')[:9]
    return render(request, 'discover_gifts.html', {'gifts': gifts})


def about(request):
    return render(request, 'about.html')


def not_authorized(request):
    return render(request, 'not_authorized.html')


def profile(request, id):
    profile = User.objects.get(id=id)
    return render(request, 'profile.html', {'profile': profile})


def gifts_detail(request, gift_id):
    gift = Gift.objects.get(id=gift_id)
    comments = Comment.objects.filter(gift=gift)
    comment_form = CommentForm()
    return render(request, 'gifts/detail.html', {'gift': gift, 'comment_form': comment_form, 'comments': comments})


@login_required
def add_comment(request, gift_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.user = request.user
        new_comment.gift_id = gift_id
        new_comment.save()
    return redirect('gifts_detail', gift_id=gift_id)


def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    gift_id = comment.gift_id
    comment.delete()
    return redirect('gifts_detail', gift_id=gift_id)


def search(request):
    query = request.GET.get('search', '')
    search = User.objects.filter(username__contains=query)
    return render(request, 'search.html', {'search': search})

    # Authentication views


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username=u, password=p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    print("The account has been disabled.")
                    return redirect('/')
            else:
                print("The username and/or password is incorrect.")
                return redirect('/login')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


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


@method_decorator(login_required, name='dispatch')
class GiftCreate(CreateView):
    model = Gift
    fields = ['description']

    def form_valid(self, form):
        gift = form.instance
        gift.user = self.request.user
        photo_file = self.request.FILES.get('photo-file', None)
        if photo_file:
            s3 = boto3.client('s3')
            key = uuid.uuid4().hex[:6] + \
                photo_file.name[photo_file.name.rfind('.'):]
            try:
                s3.upload_fileobj(photo_file, BUCKET, key)
                photo_url = f"{S3_BASE_URL}{BUCKET}/{key}"
                gift.photo_url = photo_url
            except:
                print('An error occurred uploading file to S3')
        gift.save()
        return redirect(f"/profile/{self.request.user.id}")


@method_decorator(login_required, name='dispatch')
class GiftUpdate(UpdateView):
    model = Gift
    fields = ['description']

    def form_valid(self, form):
        gift = form.instance
        if gift.user != self.request.user:
            return redirect('/not_authorized')
        photo_file = self.request.FILES.get('photo-file', None)
        if photo_file:
            s3 = boto3.client('s3')
            key = uuid.uuid4().hex[:6] + \
                photo_file.name[photo_file.name.rfind('.'):]
            try:
                s3.upload_fileobj(photo_file, BUCKET, key)
                photo_url = f"{S3_BASE_URL}{BUCKET}/{key}"
                gift.photo_url = photo_url
            except:
                print('An error occurred uploading file to S3')
        gift.save()
        return redirect(f"/profile/{self.request.user.id}")


@method_decorator(login_required, name='dispatch')
class GiftDelete(DeleteView):
    model = Gift

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user == request.user:
            self.object.delete()
            return redirect(f"/profile/{self.request.user.id}")
        else:
            return redirect('/not_authorized')


@method_decorator(login_required, name='dispatch')
class CommentUpdate(UpdateView):
    model = Comment
    fields = ['text']

    def get_success_url(self, **kwargs):
        return f"/gifts/{self.object.gift_id}"
