from user_borrowAndReturn.models import Book, Category, BorrowingRecord
from django.db.models import Count, F
from django.shortcuts import render, redirect, HttpResponse,  get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
    # try:
        book=Book.objects.get(id=id)
        if book is not None:
            result=f"<h2>{book.title}</h2>"
            borrow_count=BorrowingRecord.objects.count()
            result += f"<img src='{book.cover}' alt='Book Cover' style='width: 100px;'><br><p>類型:<a href='/category/{book.category_id}'>{book.category}</a></p><p>作者:{book.author}</p><p>館內餘量:{book.available_quantity}   借閱量：{borrow_count}</p>"
            return render(request, 'bookPage.html', {'book':book})
    # except:
    #     return redirect('/')

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
            return render(request, 'categoryPage.html', {'books':books,'category':category})
    except:
        return redirect('/')

def search(request):
    kw = request.GET.get('keyWord')
    books = Book.objects.filter(title__icontains=kw) | Book.objects.filter(author__icontains=kw)
    return render(request, 'search_results.html', {'books': books, 'keyWord': kw})

def borrowBook(request, book_id):
    if request.user.is_active:
        book = get_object_or_404(Book, id=book_id)
        if BorrowingRecord.objects.filter(user=request.user,book=book,is_returned=False,).exists():
            return render(request, 'borrow_view.html', {'msg': '已經借閱本圖書'})
        if book.available_quantity > 0:
            due_date = timezone.now() + timezone.timedelta(days=90)

            borrowing_record = BorrowingRecord.objects.create(
                user=request.user,
                book=book,
                borrowing_date=timezone.now(),
                due_date=due_date,
                is_returned=False, 
            )
            book.available_quantity -= 1
            book.save()
            return render(request, 'borrow_view.html', {'borrowing_record': borrowing_record,'msg':'借閱成功！'})
        else:
            return render(request, 'borrow_view.html', {'msg': '圖書暫不可借'})
    
    else:
        messages.warning(request, '尚未登入不可借書，請先登入')
        return redirect('login')