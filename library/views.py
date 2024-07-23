"""
Module docstring: This module contains API views for managing books and loans.
"""

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import BlacklistedToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.parsers import MultiPartParser, FormParser

from django.contrib.auth.models import User
from .models import Book, Loans
from .serializers import BookSerializer, LoanSerializer

from django.contrib.auth import logout as django_logout

@api_view(['GET'])
def index(request):
    """
    Simple API endpoint to return a hello message.
    """
    return Response({'msg': 'hello'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_member(request):
    """
    Example API endpoint accessible only to authenticated users.
    """
    return Response({'msg': 'test'})

@api_view(['POST'])
def register(request):
    """
    API endpoint to register a new user.
    """
    required_fields = ['username', 'email', 'password']
    missing_fields = [field for field in required_fields if field not in request.data]

    if missing_fields:
        return Response({'error': f'Missing required fields: {", ".join(missing_fields)}'})

    try:
        user = User.objects.create_user(
            username=request.data['username'],
            email=request.data['email'],
            password=request.data['password']
        )
        user.is_active = True
        user.save()

        return Response({'msg': 'User registered successfully'})
    
    except Exception as e:
        return Response({'error': str(e)})

@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def book_view(request, id=None):
    parser_classes = (MultiPartParser, FormParser)

    if request.method == 'GET':
        if id is not None:
            try:
                book = Book.objects.get(id=id, active=True)
                return Response(BookSerializer(book).data)
            except Book.DoesNotExist:
                return Response({'error': 'Book not found'}, status=404)
        else:
            books = Book.objects.filter(active=True)
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Book added successfully"})
        return Response(serializer.errors)
    
    elif request.method == 'DELETE':
        try:
            book = Book.objects.get(id=id)
            book.active = False
            book.save()
            return Response({'msg': 'Book deleted successfully'})
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=404)
    
    elif request.method == 'PUT':
        try:
            book = Book.objects.get(id=id)
            serializer = BookSerializer(book, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Book updated successfully'})
            return Response(serializer.errors)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def loan(request, id):
    """
    API endpoint to create a new loan for a book.
    """
    try:
        user = request.user
        book = Book.objects.get(id=id)
        if book.active:
            new_loan = Loans.objects.create(UserID=user.id, BookID=book.id, active=True)
            book.active = False
            book.save()
            new_loan.save()
            return Response({"msg": "Loan created successfully"})
        else:
            return Response({"error": "Book is not available for loan"})
    except Exception as e:
        return Response({"error": str(e)})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def returnBook(request, id):
    """
    API endpoint to return a loaned book.
    """
    try:
        user = request.user
        book = Book.objects.get(id=id)
        loan = Loans.objects.get(BookID=book.id, UserID=user.id, active=True)
        loan.active = False
        book.active = True
        loan.save()
        book.save()
        return Response({"msg": f"Book '{book.bName}' returned successfully"})
    except Exception as e:
        return Response({"error": str(e)})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def showLoans(request):
    loans = Loans.objects.all().filter(UserID = request.user.id, active=True)
    return Response(LoanSerializer(loans, many=True).data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        # Get the access token from the request headers
        authorization_header = request.headers.get('Authorization')
        print(authorization_header)
        if not authorization_header or 'Bearer ' not in authorization_header:
            raise AuthenticationFailed('Invalid authorization header')

        access_token = authorization_header.split()[1]  # Extracting the token from 'Bearer <token>'
        print(access_token)

        # Add the token to the blacklist
        # token = BlacklistedToken(token=access_token)
        # token.save()

        # Perform logout (optional, depending on your application logic)
        django_logout(request)

        return Response({'message': 'Logout successful'}, status=200)

    except AuthenticationFailed as e:
        return Response({'error': str(e)}, status=401)  # Unauthorized
    except Exception as e:
        return Response({'error': str(e)}, status=500)