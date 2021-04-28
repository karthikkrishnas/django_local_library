from django.urls import path
from catalog import views

urlpatterns=[
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name = 'books'),
    path('books/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name = 'authors'),
    path('authors/<int:pk>', views.AuthorDetailView.as_view(), name = 'author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name = 'my-borrowed'),
    path('borrowed/', views.AllBorrowedBooksListView.as_view(), name = 'all-borrowed'),
    path('books/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('authors/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('authors/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('authors/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
    path('books/create/', views.BookCreate.as_view(), name='book-create'),
    path('books/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
    # for challenge:
    # re_path(r'^book/?year=(?P<year>\d+)&month=(?P<month>\d+)&day=(?P<day>\d+)$',view function, name='xyz'),
]

