"""cpanel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.display),
    url(r'^signIn/',views.signIn, name="signIn"),
    url(r'^postsign/',views.postsign),
    url(r'^logout/',views.logout,name="log"),
    url(r'^signUp/',views.signUp, name="signUp"),
    url(r'^postsignUp',views.postsignUp, name="postsignUp"),
    url(r'^shoplist/',views.shoplist,name="shoplist"),
    url(r'^orderdetails/',views.orderdetails,name="orderdetails"),
    url(r'^thankyou/',views.thankyou,name="thankyou"),
    url(r'^acceptmail/',views.acceptmail,name="acceptmail"),
    url(r'^rejectmail/',views.rejectmail,name="rejectmail"),
    url(r'^process_order/',views.process_order,name="porcess_order"),
]
