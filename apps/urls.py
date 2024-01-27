from django.conf import urls
from django.contrib.auth.views import LogoutView
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import path

from apps.tasks import task_send_email
from apps.views import IndexView, CustomLoginView, RegisterLoginView, BlogDetailView, BlogListView, EmailView


def send_email_task(req):
    task_send_email.delay('math', 'base',
                          ['najmiddinovavaz2208@gmail.com', 'bexruzpdp01@gmail.com', 'aralovjavoxir@gmail.com',
                           'fayzullaxojaevi@gmail.com'])
    return JsonResponse({"success": True})


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('blog-list', BlogListView.as_view(), name='blog_list_page'),
    path('blog-detail/<int:pk>', BlogDetailView.as_view(), name='blog_detail_page'),
    path('register/', RegisterLoginView.as_view(), name='register_page'),
    path('login', CustomLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('newletter/', EmailView.as_view(), name="newsletter"),
    path('send', send_email_task)
]


def page_404(request, exception):
    return render(request, 'apps/404.html', status=404)


urls.handler404 = 'apps.urls.page_404'
