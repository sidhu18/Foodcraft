"""fire URL Configuration

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
from django.conf.urls import url
from . import views

app_name = 'accounts'

urlpatterns = [
    url(r'^$',views.signIn),
    url(r'^postsign/',views.postsign),
    url(r'^logout/',views.logout,name="logout"),
    url(r'^signup/',views.signUp,name='signup'),
    url(r'^postsignup/',views.postsignup,name='postsignup'),
    url(r'^post_add_category/', views.post_add_category, name='post_add_category'),
    url(r'^add_category/', views.add_category, name='add_category'),
    url(r'^create/',views.create,name='create'),
    url(r'^post_create/',views.post_create,name='post_create'),
    url(r'^check_categories/',views.check_categories,name='check_categories'),
    url(r'^post_check/',views.post_check,name='post_check'),
    url(r'^post_pre_update/', views.post_pre_update, name='post_pre_update'),
    url(r'^post_update/', views.post_update, name='post_update'),
    url(r'^post_remove/', views.post_remove, name='post_remove'),
    url(r'^new_orders/', views.view_new_orders, name='view_new_orders'),
    url(r'^order_taken/', views.order_taken, name='order_taken'),
    url(r'^view_completed_orders/', views.view_completed_orders, name='view_completed_orders'),

]

