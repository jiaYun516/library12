from user_borrowAndReturn.models import Member, Book, Category, BorrowingRecord
from django.db.models import Count, F
from django.shortcuts import render, redirect, HttpResponse

'''
annotate(borrow_count=Count('borrowingrecord')): 為每本書加上借閱量計算的項目
book對象調用count方法計算此book對象在borrowingrecord表中的次數
.order_by('-borrow_count', 'title'): 依照borrow_count降序 title升序
'''
def homepage(request):
    books = Book.objects.annotate(borrow_count=Count('borrowingrecord')).order_by('-borrow_count', 'title')
    return render(request, 'homePage.html', {'books':books})

'''
不會有同id的書所以不需要遍歷
'''
def searchById(request, id):
    try:
        book=Book.objects.get(id=id)
        if book is not None:
            result=f"<h2>{book.title}</h2>"
            borrow_count=BorrowingRecord.objects.count()
            result += f"<img src='{book.cover}' alt='Book Cover' style='width: 100px;'><br><p>類型:<a href='/category/{book.category_id}'>{book.category}</a></p><p>作者:{book.author}</p><p>館內餘量:{book.available_quantity}   借閱量：{borrow_count}</p>"
            return render(request, 'bookPage.html', {'book':book})
    except:
        return redirect('/')

'''
filter(category_id=category_id):filter方法會抓取所有符合條件的資料

'''
def searchByCategory(request, category_id):
    try:
        books=Book.objects.filter(category_id=category_id).annotate(borrow_count=Count('borrowingrecord')).order_by('-borrow_count', 'title')
        if books:
            category = books.first().category
            result=f"<h2>{category}</h2>"
            for book in books:
                result += f"<p>{book.title}</p> <p>作者:{book.author}</p> <p>館內餘量:{book.available_quantity}   借閱量：{book.borrow_count}</p><br>"
            return HttpResponse(result)
    except:
        return redirect('/')
