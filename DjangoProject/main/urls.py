from django.conf.urls import patterns, url
from main import views
from main.views import (
    IndexView,
    ProfileView,
    LibraryListView,
    LibraryCreate,
    LibraryDetailView,
    BookDetailView,
    BookCreate,
    BookDelete)

urlpatterns = patterns('',
                       url(r'^$', IndexView.as_view(), name='index'),
                       url(r'^profile/$', ProfileView.as_view(),
                           name='profile'),
                       url(r'^register/$', views.register, name='register'),
                       url(r'^login/$', views.user_login, name='login'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^library/list/$',
                           LibraryListView.as_view(), name='library-list'),
                       url(r'^library/new/$',
                           LibraryCreate.as_view(), name='library-new'),
                       url(r'^library/(?P<pk>\d+)/$',
                           LibraryDetailView.as_view(),
                           name='library-detail'),
                       url(r'^book/(?P<slug>[-\w]+)/$',
                           BookDetailView.as_view(),
                           name='book-detail'),
                       url(r'^library/(?P<pk>\d+)/new/$',
                           BookCreate.as_view(),
                           name='book-new'),
                       url(r'^book/(?P<slug>[-\w]+)/delete/$',
                           BookDelete.as_view(),
                           name='book-delete'),
                       url(r'^books/edit/$',
                           views.BookEdit, name='edit-books')
                       )
