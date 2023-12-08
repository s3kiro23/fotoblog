"""fotoblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import authentication
from django.contrib import admin, messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import blog.views
from authentication.views import CustomPasswordChangeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True,
    ), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('recovery-password/', PasswordResetView.as_view(
        template_name='authentication/recovery-password.html',
        success_url='/',
    ), name='recovery-password'),
    path('change-password/', CustomPasswordChangeView.as_view(
        template_name='blog/change-password.html',
        success_url='/home/',
    ), name='change-password'),
    path('home/', blog.views.home, name='home'),
    path('profile/', authentication.views.profile_page, name='profile_page'),
    path('profile/edit/', authentication.views.edit_profile, name='edit_profile'),
    path('account/disable/', authentication.views.disable_account, name='disable_account'),
    path('follow-users/', blog.views.follow_users, name='follow_users'),
    path('my-photos/', blog.views.my_photos, name='my_photos'),
    path('photo/upload/', blog.views.photo_upload, name='photo_upload'),
    path('photo/<int:photo_id>/', blog.views.photo_detail, name='photo_detail'),
    path('photo/<int:photo_id>/edit', blog.views.edit_photo, name='edit_photo'),
    path('photo/upload-multiple/', blog.views.create_multiple_photos, name='create_multiple_photos'),
    path('profile/photo/upload', authentication.views.upload_profile_photo, name='profile_photo_upload'),
    path('blog/create', blog.views.blog_and_photo_upload, name='blog_create'),
    path('blog/<int:blog_id>', blog.views.view_blog, name='view_blog'),
    path('blog/<int:blog_id>/edit', blog.views.edit_blog, name='edit_blog'),
    path('signup/', authentication.views.signup_page, name='signup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
