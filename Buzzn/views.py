from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile,Buzz
from .forms import BuzzForm, SignUpForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        form = BuzzForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                buzz = form.save(commit=False)
                buzz.user = request.user
                buzz.save()
                messages.success(request,("Your Buzz has been Posted!"))
                return redirect('home')
        buzzes = Buzz.objects.all().order_by("-created_at")
        return render(request, 'home.html',{'buzzes':buzzes,"form":form})
    else:
        buzzes = Buzz.objects.all().order_by("-created_at")
        return render(request, 'home.html',{'buzzes':buzzes})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request,'profile_list.html',{'profiles':profiles})
    else:
        messages.success(request,("You Must Be Logged In To View This Page..."))
        return redirect('home')
    
def unfollow(request,pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        request.user.profile.follows.remove(profile)
        request.user.profile.save()
        messages.success(request,(f"You have Successsfully Unfollowed {profile.user.username}"))
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request,("You Must Be Logged In To View This Page..."))
        return redirect('home')
    
def follow(request,pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        request.user.profile.follows.add(profile)
        request.user.profile.save()
        messages.success(request,(f"You have Successsfully Followed {profile.user.username}"))
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request,("You Must Be Logged In To View This Page..."))
        return redirect('home')
    
def profile(request,pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        buzzes = Buzz.objects.filter(user_id=pk).order_by("-created_at")
        if request.method=="POST":
            current_user_profile = request.user.profile
            action = request.POST['follow']
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            current_user_profile.save()
        return render(request,'profile.html',{'profile':profile,'buzzes':buzzes})
    else:
        messages.success(request,("You Must Be Logged In To View This Page..."))
        return redirect('home')
    
def followers(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user__id=pk)
            return render(request,'followers.html',{'profiles':profiles})
        else:
            messages.success(request,("That's not Your Profile Page..."))
            return redirect('home')
    else:
        messages.success(request,("You Must Be Logged In To View This Page..."))
        return redirect('home')
    
def follows(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user__id=pk)
            return render(request,'follows.html',{'profiles':profiles})
        else:
            messages.success(request,("That's not Your Profile Page..."))
            return redirect('home')
    else:
        messages.success(request,("You Must Be Logged In To View This Page..."))
        return redirect('home')
    
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,("You have been Logged In! Get Buzz'n!!"))
            return redirect('home')
        else:
            messages.success(request,("There was an error loggin in. Please try again..."))
            return redirect('login')
    else:    
        return render(request,'login.html',{})


def logout_user(request):
    logout(request)
    messages.success(request,("You Have Been Logged Out. Buzz Later! "))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user=authenticate(username=username, password=password)
            login(request,user)
            messages.success(request,("You Have Successfully Registered. Welcome!!"))
            return redirect('home')

    return render(request,"register.html",{'form':form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)
    
        user_form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user)
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            login(request, current_user)
            messages.success(request,("Your Profile Has been Updated!"))
            return redirect('home')
        return render(request,"update_user.html",{'user_form':user_form, 'profile_form':profile_form})
    else:
        messages.success(request,("You must be Logged In to view that page"))
        return redirect('home')
    
def buzz_like(request, pk):
    if request.user.is_authenticated:
        buzz = get_object_or_404(Buzz, id=pk)
        if buzz.likes.filter(id=request.user.id):
            buzz.likes.remove(request.user)
        else:
            buzz.likes.add(request.user)
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request,("You must be Logged In to view that page"))
        return redirect('home')
    
def buzz_share(request, pk):
    buzz = get_object_or_404(Buzz, id=pk)
    if buzz:
        return render(request,"buzz_share.html",{'buzz':buzz})
    else:
        messages.success(request,("That buzz does not exist..."))
        return redirect('home')
    
def delete_buzz(request,pk):
    if request.user.is_authenticated:
        buzz = get_object_or_404(Buzz, id=pk)
        if request.user.username == buzz.user.username:
            buzz.delete()
            messages.success(request, ("The Buzz Has Been Deleted!"))
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.success(request,("You Don't Own That Buzz!!"))
            return redirect('home')
    else:
        messages.success(request,("Please Login to continue..."))
        return redirect(request.META.get("HTTP_REFERER"))

def edit_buzz(request,pk):
    if request.user.is_authenticated:
        buzz = get_object_or_404(Buzz, id=pk)
        if request.user.username == buzz.user.username:
            form = BuzzForm(request.POST or None, instance=buzz)
            if request.method == "POST":
                if form.is_valid():
                    buzz = form.save(commit=False)
                    buzz.user = request.user
                    buzz.save()
                    messages.success(request,("Your Buzz has been Updated!"))
                    return redirect('home')
            else:
                return render(request,"edit_buzz.html",{'form':form, 'buzz':buzz})
        else:
            messages.success(request,("You Don't Own That Buzz!!"))
            return redirect('home')
    else:
        messages.success(request,("Please Login to continue..."))
        return redirect('home')
         
def search(request):
    if request.method == "POST":
        search = request.POST['search']
        searched = Buzz.objects.filter(username__contains = search)
        return render(request,'search.html',{'search':search, 'searched':searched})
    else:
        return render(request,'search.html',{})
    
def search_user(request):
    if request.method == "POST":
        search = request.POST['search']
        searched = User.objects.filter(username__contains = search)
        return render(request,'search_user.html',{'search':search, 'searched':searched})
    else:
        return render(request,'search_user.html',{})