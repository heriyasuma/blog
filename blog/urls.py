from django.urls import path
from . views import (
    post_list_view,
    post_detail_view,
    categorie_list_view,
    categorie_detail_view,
    tag_list_view,
    tag_detail_view,
    tag_create_view,
    search_results_view,
    )


urlpatterns = [
    path('', post_list_view, name='post-list'),
    path('<slug:slug>', post_detail_view, name='post-detail'),
    path('categorie/', categorie_list_view, name='categorie-list'),
    path('categorie/<slug:slug>', categorie_detail_view, name='categorie-detail'),
    path('tag', tag_list_view, name='tag-list'),
    path('tag/<slug:slug>', tag_detail_view, name='tag-detail'),
    path('tag/create/item', tag_create_view, name='tag-create'),
    path('search/', search_results_view, name='search-results'),
]
