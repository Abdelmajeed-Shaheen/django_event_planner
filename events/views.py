from datetime import datetime
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.forms.widgets import HiddenInput
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import *
from .models import *

def home(request):
    return render(request, 'home.html')

def event_list(request):
    events = Event.objects.filter(date__gte=datetime.today())
    query = request.GET.get('q')
    if query:
        events = events.filter(Q(title__icontains=query)|Q(description__icontains=query)|Q(organizer__username__icontains=query)).distinct()
    paginator = Paginator(events,6)
    pagenumber = request.GET.get('page')
    pageobj = paginator.get_page(pagenumber)
    context = {
        "events":pageobj
        }
    return render(request, 'event_list.html',context)


def dashboard(request):
    if request.user.is_authenticated:
        events = Event.objects.filter(organizer=request.user)
        query = request.GET.get('q')
        if query:
            events = events.filter(Q(title__icontains=query)).distinct()
        paginator = Paginator(events,3)
        pagenumber = request.GET.get('page')
        pageobj = paginator.get_page(pagenumber)
        context = {
            "events":pageobj
            }
        return render(request, 'dashboard.html',context)
    return redirect("login")

def event_detail(request,event_id ):
    event_obj = Event.objects.get(id = event_id)
    context = {
    "event": event_obj
    }
    return render(request, 'event_detail.html', context)


#event CRUD functions
def event_update(request, event_id):
    event_obj = Event.objects.get(id = event_id)
    if request.user == event_obj.organizer:
        form = EventUpdate(instance = event_obj)
        if request.method=="POST":
            form = EventUpdate(request.POST, request.FILES, instance = event_obj)
            if form.is_valid():
                form.save()
                return redirect('event-detail', event_id)
        context = {
        "event": event_obj,
        'form': form,
        }
        return render(request, 'event_update.html', context)
    return redirect('login')

def event_create(request):
    form = EventUpdate()
    if request.method=="POST":
        form = EventUpdate(request.POST, request.FILES)
        if form.is_valid():
            event=form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('dashboard')
    context = {
    'form': form,
    }
    return render(request, 'event_create.html', context)

def event_delete(request , event_id):
    event_obj = Event.objects.get(id = event_id)
    if request.user == event_obj.organizer:
        event_obj.delete()
        return redirect('dashboard')
    return redirect('login')


# User CRUD functions
class Signup(View):
    form_class = UserSignup
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, "You have successfully signed up.")
            login(request, user)
            return redirect("home")
        messages.warning(request, form.errors)
        return redirect("signup")


class Login(View):
    form_class = UserLogin
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, "Welcome Back!")
                return redirect('dashboard')
            messages.warning(request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")
