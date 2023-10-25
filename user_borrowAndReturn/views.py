from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from user_borrowAndReturn.models import Member, Book
from django.db.models import Count, F

# Create your views here.
def homepage(request):
    books = Book.objects.annotate(borrow_count=Count('borrowingrecord')).order_by('-borrow_count', 'title')
    result = "<h1>The hottest books</h1>"
    for book in books:
        borrow_count = book.borrowingrecord_set.count()
        result += f"<a href='/book/{book.slug}'>{book.title}</a> <p>類型:{book.category}</p><p>作者:{book.author}</p>借閱量：{borrow_count}</p>"

    return HttpResponse(result)

def showBook(request, slug):
    try:
        book=Book.objects.get(slug=slug)
        if book != None:
            borrow_count = book.borrowingrecord_set.count()
            result=f"<h2>{book.title}</h2>"
            result += f"<img src='{book.cover}' alt='Book Cover' style='width: 100px;'><br><p>類型:{book.category}</p><p>作者:{book.author}</p><p>館內餘量:{book.available_quantity}   借閱量：{borrow_count}</p>"
            return HttpResponse(result)
    except:
        return redirect('/')