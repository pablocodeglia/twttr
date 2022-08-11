import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator
from django.db.models import F
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import prefetch_related_objects
from .forms import PostForm

from .models import User, Post


def index(request):
    all_posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'all_posts':all_posts,
        'page_obj':page_obj
    }

    return render(request, "network/index.html", context)

@csrf_exempt
@login_required
def following_view(request):
    following_userlist = request.user.following.values_list('pk', flat=True)
    all_posts = Post.objects.filter(user__in=following_userlist).order_by('-timestamp')
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'all_posts':all_posts,
        'page_obj':page_obj
    }

    return render(request, "network/following.html", context)

@csrf_exempt
def profile_view(request, id):
    # Ger User
    user_profile = User.objects.get(pk=id)

    # Define Paginator
    all_posts = Post.objects.filter(user_id = id).order_by('-timestamp')
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Followers count
    followers_count = User.objects.filter(following__id = id).count()
    # Following count
    following_count = user_profile.following.count()
    is_following = request.user.following.filter(id=user_profile.id).exists()
    context = {
        'user_profile': user_profile,
        'is_following': is_following,
        'following_count': following_count,
        'followers_count': followers_count,
        'page_obj': page_obj,
    }
    return render(request, "network/profile.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@csrf_exempt
@login_required
def like(request, post_id):
    post = Post.objects.get(pk = post_id)

    if request.method == "POST":
        if post.likes.filter(id = request.user.id).exists():
            post.likes.remove(request.user)
            post.refresh_from_db()
            post.likes_num = F('likes_num') - 1
            post.save()
            likes_count = post.likes.count()
            likes_this = False
        else:
            post.likes.add(request.user)
            post.refresh_from_db()
            post.likes_num = F('likes_num') + 1
            post.save()
            likes_count = post.likes.count()
            likes_this = True

        return JsonResponse({
            "likes_this": likes_this,
            "likes_count":likes_count,
        })            
            

@csrf_exempt
@login_required
def follow_user(request, id):
    if request.method == "POST":
        user_to_follow = User.objects.get(pk=id)
        current_user = User.objects.get(pk=request.user.id)

        if current_user.following.filter(id=user_to_follow.id).exists():
            # user_to_follow.followers.remove(current_user)
            current_user.following.remove(user_to_follow)
            followers_count = User.objects.filter(following__id = id).count()

            return JsonResponse({
                "is_following": False,
                "followers": followers_count
            })
        else:
            # user_to_follow.followers.add(current_user)
            current_user.following.add(user_to_follow)
            followers_count = User.objects.filter(following__id = id).count()

            return JsonResponse({
                "is_following": True,
                "followers": followers_count
            })


@login_required
def new_post_view(request):

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid:
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return HttpResponseRedirect(reverse('index'))

    else:
        form = PostForm()

    return render(request, "network/new_post.html", {'form':form})


@csrf_exempt
@login_required        
def edit_post_view(request, id):
    post = Post.objects.get(pk=id)
    if request.method == "POST":
        data = json.loads(request.body)
        post.body = data['text']
        post.save()
        return JsonResponse({
                    "body": post.body
                })
    else:
        return JsonResponse({
                    "body": post.body
                })