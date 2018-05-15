from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from .forms import PostForm
from .models import Post

# Create your views here.

def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # if success
        messages.success(request, 'Succesfully Created')
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, 'post_form.html', context)

def post_detail(request, id=1):

    instance = get_object_or_404(Post, id=id)

    context = {
        "title": "Detail",
        "post": instance
    }

    return render(request, 'post_detail.html', context)


def post_list(request):

    queryset_list = Post.objects.all()
    paginator = Paginator(queryset_list, 5)

    page = request.GET.get('page')

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
        "title": "Posts List",
        "post_list": queryset
    }
    return render(request, 'post_list.html', context)


def post_update(request, id=None):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # if success
        messages.success(request, 'Succesfully Saved')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "post": instance,
        "form": form
    }
    return render(request, 'post_form.html', context)


def post_delete(request, id=None):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, 'Succesfully Deleted')
    return redirect('posts:list')