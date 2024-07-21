from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Book
from .serializers import BookSerializer

@api_view(['GET'])
def index(request):
    return Response({'msg':'hello'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_member(request):
    return Response({'msg':'test'})

@api_view(['POST', 'GET', 'DELETE', 'PUT'])
def book_view(request, id=None):
    if request.method == 'GET':
        if id is not None:
            try:
                book = Book.objects.get(id=id, active = True)
                return Response(BookSerializer(book).data)
            except Book.DoesNotExist:
                return Response({'error': 'Book not found'}, status=404)
        else:
            books = Book.objects.all().filter(active=True)
            return Response(BookSerializer(books, many=True).data)
    
    if request.method == 'POST':
        book = BookSerializer(data=request.data)
        if book.is_valid():
            book.save()
            return Response ({"book added": request.data['bName']})
        else:
            return Response (book.errors)
    
    if request.method == 'DELETE':
        book = Book.objects.get(id=id)
        book.active = 0
        book.save()
        return Response({'book was deleted': request.data['bName']})
    
    if request.method == 'PUT':
        book = Book.objects.get(id=id)
        ser = BookSerializer(data=request.data)
        old_task = Book.objects.get(id=id)
        ser.update(old_task, request.data)
        return Response({'book updated': 'test'})