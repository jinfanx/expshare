"""expshare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path,re_path
from expshare import views
from haystack import urls
from django.conf.urls import url,include

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('admin/', admin.site.urls),
    path('direct/<str:template>',views.direct),
    path('index/',views.IndexView.as_view()),
    path('newcategory/',views.newcategory),
    path('addcategory/',views.addcategory),
    path('newshare/',views.newshare),
    path('addshare/',views.addshare),
    path('list_share/<str:category>/',views.list_shares),
    path('goregister/',views.GoRegisterView.as_view()),
    path('register/',views.register),
    path('active_acct/<str:email>/',views.active_acct),
    path('check_username/',views.check_username),
    path('check_email/',views.check_email),
    path('go_login/',views.go_login),
    path('login/',views.login),
    path('logout/',views.logout),
    path('my_note/',views.my_note),
    path('praise/',views.praise),
    path('feedback/',views.feedback),
    # url(r'^search/', include(urls)),
    url(r'search/',views.MySeachView()),
]
