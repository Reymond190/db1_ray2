"""db1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, re_path
from django.conf.urls import url
from rest_framework import routers
from one import views
from django.urls import include, path
from rest_it.views import RegisterView, CustomLoginView




router = routers.DefaultRouter()
router.register(r'groups', views.ApiViewSet)
router.register(r'api2', views.SingleApi)



urlpatterns = [
    # url(r'^$', views.UsersListView.as_view(), name='users_list'),
    # url(r'^run/$', views.fun1, name='generate'),
    url(r'^rest-auth/login/', CustomLoginView.as_view()),
    # url(r'^rest-auth/registration/', RegisterView.as_view()),
    # url(r'^rest-auth/', include('rest_auth.urls')),
    path('admin/', admin.site.urls),
    path('sun/',views.all2),
    url('^extendapi/(?P<vin>.+)/$',views.Myfilter.as_view()),
    path('extendapi/',views.Myfilter2.as_view()),
    path('api2/', views.ClassicList.as_view()),
    url('^path/(?P<vin>.+)/$', views.FilterList.as_view()),
    path('path/', views.FilterList2.as_view()),
    path('tickets/',views.TicketView.as_view()),
    re_path(r'^tickets/(?P<pk>[0-9]+)$', # Url to get update or delete a movie
        views.Ticketupdate.as_view(),

    ),

]

