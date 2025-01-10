from rest_framework import serializers
from .models import CustomUser,Book,Transaction

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'date_of_membership', 'active_status']
        read_only_fields = ['date_of_membership']

class CustomUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email','date_of_membership', 'password', 'active_status']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Use the custom user manager to create a new user
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            active_status=validated_data.get('active_status', True),
        )
        return user
    
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
        read_only_fields = ['id']


class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Shows the user's email instead of ID
    book = serializers.StringRelatedField(read_only=True)  # Shows the book's title instead of ID

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'book', 'borrowed_date', 'returned_date']
        read_only_fields = ['id', 'borrowed_date', 'returned_date']

class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['user', 'book']

    def validate(self, data):
        # Check if the book has copies available
        book = data['book']
        if book.copies_available <= 0:
            raise serializers.ValidationError(f"The book '{book.title}' is not available.")
        
        # Ensure the user hasn't already checked out the same book
        user = data['user']
        if Transaction.objects.filter(user=user, book=book, returned_date__isnull=True).exists():
            raise serializers.ValidationError(f"The user '{user.username}' has already checked out this book.")

        return data

    def create(self, validated_data):
        # Reduce the number of copies available when a book is checked out
        book = validated_data['book']
        book.copies_available -= 1
        book.save()

        return super().create(validated_data)
