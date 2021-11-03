from django.urls import path

from . import views

app_name = 'posts'


urlpatterns = [
    path('', views.index, name='index'),
    path('groups/', views.groups, name='groups'),
    path('group/<slug:slug>/', views.group_posts, name='group_list'),
    path('create/', views.post_create, name='post_create'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('feedback/', views.feedback, name='feedback'),
    path('feedback/done/', views.feedback_done, name='feedback_done'),
    path('votepost/', views.votepost, name='votepost'),
]
