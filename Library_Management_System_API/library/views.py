from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone
#from django_filters.rest_framework import DjangoFilterBackend
#from rest_framework.filters import SearchFilter

from .models import CustomUser, Book, Transaction
from .serializers import (
    CustomUserSerializer,
    CustomUserCreateSerializer,
    BookSerializer,
    TransactionSerializer,
    TransactionCreateSerializer,
)


# Admin-only view to list all users
class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]  # Only admins can view all users
    authentication_classes = [JWTAuthentication]  # JWT Authentication


# Public view for user registration
class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserCreateSerializer
    permission_classes = [permissions.AllowAny]  # Open for user registration
    authentication_classes = [JWTAuthentication]


# View for users to retrieve their details
class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can view their details
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        # Allow users to see only their details
        return CustomUser.objects.filter(id=self.request.user.id)


# ViewSet for managing books
"""class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_fields = ['title', 'author', 'isbn', 'copies_available']
    search_fields = ['title', 'author', 'isbn']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]  # Only admins can modify books
        return [permissions.AllowAny()]  # All users can view books"""

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated] 
    authentication_classes = [JWTAuthentication]

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can view book details
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        # Allow to view details of each book
        book_id = self.kwargs.get('pk')
        return Book.objects.filter(id=book_id)

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

class BookUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        book_id = self.kwargs.get('pk')
        return Book.objects.filter(id=book_id)


# View for listing a user's transactions
class TransactionListView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can view transactions
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        # Allow users to view only their transactions
        return Transaction.objects.filter(user=self.request.user)


# View for borrowing a book
class BorrowBookView(generics.CreateAPIView):
    serializer_class = TransactionCreateSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can borrow books
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# View for returning a book
"""class ReturnBookView(generics.UpdateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can return books
    authentication_classes = [JWTAuthentication]

    def update(self, request, *args, **kwargs):
        transaction = self.get_object()

        # Ensure only the user who borrowed the book can return it
        if transaction.user != request.user:
            return Response({'error': 'You can only return books you borrowed.'}, status=status.HTTP_403_FORBIDDEN)

        # Mark the book as returned
        transaction.returned_date = timezone.now()
        transaction.save()

        # Increase available copies for the book
        transaction.book.copies_available += 1
        transaction.book.save()

        return Response(TransactionSerializer(transaction).data)"""
class ReturnBookView(generics.UpdateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can return books
    authentication_classes = [JWTAuthentication]

    def update(self, request, *args, **kwargs):
        transaction = self.get_object()  # Fetch the specific transaction instance based on URL parameters (e.g., pk).

        # Ensure only the user who borrowed the book can return it
        if transaction.user != request.user:
            return Response(
                {'error': 'You can only return books you borrowed.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check if the book is already returned
        if transaction.returned_date:
            return Response(
                {'error': 'This book has already been returned.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Mark the book as returned
        transaction.returned_date = timezone.now()
        transaction.save()

        # Increase available copies for the book
        transaction.book.copies_available += 1
        transaction.book.save()

        # Return the updated transaction details
        return Response(
            {"message": "Book returned successfully!", "transaction": TransactionSerializer(transaction).data},
            status=status.HTTP_200_OK
        )
