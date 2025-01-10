from django.urls import path
from .views import UserListView, UserCreateView, UserDetailView,BookUpdateDeleteView, BookListView, BookCreateView,BookDetailView,TransactionListView, BorrowBookView, ReturnBookView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/register/', UserCreateView.as_view(), name='user-create'),
    path('users/me/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/detail/<int:pk>/',BookDetailView .as_view(), name='book-l'),
    path('books/add/', BookCreateView.as_view(), name='book-create'),
    path('books/update/<int:pk>/', BookUpdateDeleteView.as_view(), name='book-update'),
    path('books/delete/<int:pk>/', BookUpdateDeleteView.as_view(), name='book-delete'),
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('transactions/borrow/', BorrowBookView.as_view(), name='borrow-book'),
    path('transactions/return/<int:pk>/', ReturnBookView.as_view(), name='return-book'),

    
]



