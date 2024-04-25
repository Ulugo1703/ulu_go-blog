from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('categories/<int:pk>', views.category_articles, name='category_articles'),
    path('articles/<int:pk>/', views.article_detail, name='detail'),
    path('login/', views.log_in, name='login'),
    path('registration/', views.sign_up, name='registration'),
    path('logout/', views.user_logout, name='logout'),

    path('create/', views.create_article, name='create'),
    path('update/<int:pk>/', views.ArticleUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.ArticleDeleteView.as_view(), name='delete'),

    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('add_vote/<str:obj_type>/<int:obj_id>/<str:action>/', views.add_vote, name='add_vote'),
    path('user_articles/', views.user_articles, name='user_articles'),
    path('search/', views.search, name='search'),

]