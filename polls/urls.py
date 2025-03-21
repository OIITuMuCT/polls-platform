"""
URL configuration for polls project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework.routers import SimpleRouter
from store.views import BookViewSet, UserBooksRelationView
from debug_toolbar.toolbar import debug_toolbar_urls
from store.views import auth

router = SimpleRouter()
router.register(r'book', BookViewSet)
router.register(r"book_relation", UserBooksRelationView)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", include("social_django.urls", namespace="social")),
    path('auth/', auth)
    # path("api-auth/", include("rest_framework.urls")),
] + debug_toolbar_urls()

urlpatterns += router.urls
