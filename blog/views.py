from django.shortcuts import render, redirect
from .models import Post, Profile
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib import messages

# Create your views here.

def home(request):
    posts = Post.objects.all()
    return render(request, "blog/index.html", {"posts": posts})


def detail(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, "blog/detail.html", {'post':post})


def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "u_form": u_form,
        "p_form": p_form
    }

    return render(request, "blog/profile.html", context)