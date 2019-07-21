"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url, include
from django.urls import path, re_path
from django.contrib import admin

from blog.views import post_list, post_detail
from config.views import links
from .custom_site import custom_site

urlpatterns = [
    path('', post_list),
    re_path('category/<int:category_id>/', post_list),
    path('tag/<int:tag_id>/', post_list),
    path('post/<int:post_id>.html', post_detail),
    path('link/', links),
    path('super_admin/', admin.site.urls),  # 用户管理后台
    path('admin/', custom_site.urls),  # 业务管理后台
]
