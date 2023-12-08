from itertools import chain

from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import formset_factory
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from . import forms
from . import models


@login_required
def home(request):
    blogs = models.Blog.objects.filter(
        Q(contributors__in=request.user.follows.all()) |
        Q(starred=True))
    photos = models.Photo.objects.filter(
        uploader__in=request.user.follows.all(),
    ).exclude(blog__in=blogs)
    blogs_and_photos = sorted(
        chain(blogs, photos),
        key=lambda instance: instance.date_created,
        reverse=True
    )

    paginator = Paginator(blogs_and_photos, 6)
    page = request.GET.get('page')

    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
    }
    return render(
        request,
        'blog/home.html',
        context=context
    )


def photo_feed(request):
    photos = models.Photo.objects.filter(
        uploader__in=request.user.follows.all()
    ).order_by('-date_created')
    return render(
        request,
        'blog/photo_feed.html',
        context={
            'photos': photos,
        }
    )


@login_required
def follow_users(request):
    form = forms.FollowUsersForm(instance=request.user)
    if request.method == 'POST':
        form = forms.FollowUsersForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(
        request,
        'blog/follow_users_form.html',
        context={'form': form}
    )


@login_required
@permission_required('blog.add_photo', raise_exception=True)
def my_photos(request):
    photos = models.Photo.objects.filter(uploader=request.user)

    paginator = Paginator(photos, 6)
    page = request.GET.get('page')

    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
    }
    return render(
        request,
        'blog/my_photos.html',
        context=context
    )


@login_required
@permission_required('blog.add_photo', raise_exception=True)
def photo_upload(request):
    form = forms.PhotoForm()
    if request.method == 'POST':
        form = forms.PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            return redirect('home')
    return render(request, 'blog/photo-upload.html', {'form': form})


@login_required
def photo_detail(request, photo_id):
    photo = get_object_or_404(models.Photo, id=photo_id)
    return render(request, 'blog/photo_detail.html', {'photo': photo})


@login_required
@permission_required('blog.change_photo', raise_exception=True)
def edit_photo(request, photo_id):
    photo = get_object_or_404(models.Photo, id=photo_id)
    edit_form = forms.PhotoForm(instance=photo)
    delete_form = forms.DeletePhotoForm()
    if request.method == 'POST':
        if 'edit_photo' in request.POST:
            edit_form = forms.PhotoForm(request.POST, request.FILES, instance=photo)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('my_photos')
        if 'delete_photo' in request.POST:
            delete_form = forms.DeletePhotoForm(request.POST)
            if delete_form.is_valid():
                photo.delete()
                return redirect('my_photos')
    return render(request, 'blog/edit_photo.html', context={'edit_form': edit_form, 'delete_form': delete_form})


@login_required
@permission_required('blog.delete_photo', raise_exception=True)
def delete_photo(request, photo_id):
    if request.method == 'POST':
        photo = get_object_or_404(models.Photo, id=photo_id)
        photo.delete()
        return redirect('home')
    return render(request, 'blog/delete-photo.html')


@login_required
@permission_required('blog.add_photo', raise_exception=True)
def blog_and_photo_upload(request):
    blog_form = forms.BlogForm()
    photo_form = forms.PhotoForm()
    if request.method == 'POST':
        blog_form = forms.BlogForm(request.POST)
        photo_form = forms.PhotoForm(request.POST, request.FILES)
        if any([blog_form.is_valid(), photo_form.is_valid()]):
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            blog = blog_form.save(commit=False)
            blog.photo = photo
            blog.author = request.user
            blog.save()
            blog.contributors.add(request.user, through_defaults={'contribution': 'Auteur principal'})
            return redirect('home')
    return render(
        request,
        'blog/create_blog_post.html',
        context={
            'blog_form': blog_form,
            'photo_form': photo_form
        }
    )


@login_required
def view_blog(request, blog_id):
    blog = get_object_or_404(models.Blog, id=blog_id)
    return render(request, 'blog/view_blog.html', {'blog': blog})


@login_required
@permission_required('blog.change_photo', raise_exception=True)
def edit_blog(request, blog_id):
    blog = get_object_or_404(models.Blog, id=blog_id)
    edit_form = forms.BlogForm(instance=blog)
    delete_form = forms.DeleteBlogForm()
    if request.method == 'POST':
        if 'edit_blog' in request.POST:
            edit_form = forms.BlogForm(request.POST, instance=blog)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')
        if 'delete_blog' in request.POST:
            delete_form = forms.DeleteBlogForm(request.POST)
            if delete_form.is_valid():
                blog.delete()
                return redirect('home')
    return render(
        request,
        'blog/edit_blog.html',
        {'edit_form': edit_form, 'delete_form': delete_form}
    )


@login_required
@permission_required('blog.add_photo')
def create_multiple_photos(request):
    PhotoFormSet = formset_factory(forms.PhotoForm, extra=5)
    formset = PhotoFormSet()
    if request.method == 'POST':
        print("post")
        formset = PhotoFormSet(request.POST, request.FILES)
        print(formset)
        if formset.is_valid():
            print("isvalid")
            for form in formset:
                print(2)
                if form.cleaned_data:
                    print(3)
                    photo = form.save(commit=False)
                    photo.uploader = request.user
                    photo.save()
            return redirect('home')
    return render(request, 'blog/create_multiple_photos.html', {'formset': formset})