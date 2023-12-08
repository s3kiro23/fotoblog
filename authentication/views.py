from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect
from django.views.generic import View

from . import forms


class CustomPasswordChangeView(PasswordChangeView):
    success_message = "Votre mot de passe a été changé avec succès."

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        errors = form.errors.get('__all__') or form.errors.get('new_password2')
        if errors:
            messages.error(self.request, errors[0])
        return response


def signup_page(request):
    form = forms.SignUpForm()
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/signup.html', context={'form': form})


def disable_account(request):
    user = request.user
    user.is_active = False
    user.save()
    messages.success(request, 'Compte désactivé avec succès.')
    logout(request)
    return redirect('login')


@login_required
def upload_profile_photo(request):
    form = forms.UploadProfilePhotoForm(instance=request.user)
    if request.method == 'POST':
        form = forms.UploadProfilePhotoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'authentication/upload-profile-photo.html', context={'form': form})


@login_required
def profile_page(request):
    User = request.user
    return render(
        request,
        'authentication/profile.html',
        context={'user': User}
    )


@login_required
def edit_profile(request):
    form = forms.ProfileForm(instance=request.user)
    if request.method == 'POST':
        form = forms.ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile_page')
    return render(
        request,
        'authentication/edit_profile.html',
        context={'form': form}
    )
