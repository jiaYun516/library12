from user_borrowAndReturn.models import Book, Category, BorrowingRecord
from django.db.models import Count, F
from django.shortcuts import render, redirect, HttpResponse,  get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import check_password
'''
annotate(borrow_count=Count('borrowingrecord')): 為每本書加上借閱量計算的項目
book對象調用count方法計算此book對象在borrowingrecord表中的次數
.order_by('-borrow_count', 'title'): 依照borrow_count降序 title升序
'''
def identity(user):
    if user.is_superuser:
        return "管理"
    elif user.is_staff:
        return "圖書員"
    else:
        return "讀者"

def homepage(request):
    books = Book.objects.annotate(borrow_count=Count('borrowingrecord')).order_by('-borrow_count', 'title')
    if request.user.is_active:
        is_superuser_staff=request.user.is_superuser or request.user.is_staff
        identityName=identity(request.user)
        return render(request, 'homePage.html', locals())
    else:
        is_superuser_staff=False
        return render(request, 'homePage.html', locals())


'''
不會有同id的書所以不需要遍歷
'''
def searchById(request, id):
    # try:
        book=Book.objects.get(id=id)
        if book is not None:
            result=f"<h2>{book.title}</h2>"
            borrow_count=BorrowingRecord.objects.count()

            if request.user.is_active:
                if BorrowingRecord.objects.filter(user=request.user,book=book,is_returned=False,).exists():
                    msg='已經借閱本圖書'
                    return render(request, 'bookPage.html', locals())
                elif book.available_quantity == 0:
                    msg='館藏已無'
                    return render(request, 'bookPage.html', locals())

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
        book = Book.objects.get(id=book_id)
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

def returnBookPage(request):
    if request.method=='POST':
        name=request.POST.get('username')
        if User.objects.filter(username=name).exists():
            user=User.objects.get(username=request.POST.get('username'))
            returnList=BorrowingRecord.objects.filter(user=user, is_returned=False).order_by('due_date')
            return render(request,'returnBookPage.html',locals())
        else:
            return render(request,'returnBookPage.html',{'msg':'查無此用戶'})

    else:
        return render(request,'returnBookPage.html',{'msg':' '})

def returnBook(request):
    if request.method=='POST':
        u=None
        returnCorrect=[]
        returnBookList=request.POST.getlist('return_books')
        for recordingId in returnBookList:
            recording=BorrowingRecord.objects.get(id=recordingId)
            recording.is_returned=True
            recording.actual_return_date=timezone.now()
            returnCorrect.append(recording)
            recording.save()

            recording.book.available_quantity += 1
            recording.book.save()
            u=recording.user
        return render(request, 'returnBook.html',{'returnCorrect':returnCorrect,
                                                  'u':u})
    else:
        return redirect('/returnBookPage/')   

@login_required
def getBorrowListByUser(request):
    borrowList=BorrowingRecord.objects.filter(user=request.user).order_by('-borrowing_date','-is_returned')
    identityName=identity(request.user)
    return render(request,'getBorrowList.html',locals())

@login_required
def getNeedReturnBook(request):
    day_now=timezone.now()
    three_days_later = day_now + timezone.timedelta(days=3)
    timeoutReturn=BorrowingRecord.objects.filter(user=request.user,
                                                 is_returned=False,
                                                 due_date__lt=day_now).order_by('due_date')
    
    needReturnList=BorrowingRecord.objects.filter(user=request.user,
                                                  is_returned=False,
                                                  due_date__lte=three_days_later).order_by('due_date')  #__gte大於等於 __lte小於等於
    identityName=identity(request.user)
    return render(request,'needReturnList.html',locals())

def librarianManagePage(request):
    if request.user.is_superuser:
        librarianList=User.objects.filter(is_staff=True, is_superuser=False)
        return render(request, 'librarianManagePage.html', locals())
    else:
        return redirect('/')

def addLibrarianPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        if User.objects.filter(username=username).exists():
            librarian=User.objects.get(username=username)
            return render(request, 'addLibrarianPage.html',locals())
        else:
            return render(request,'addLibrarianPage.html',{'msg':'查無此用戶'})
    else:
        return render(request, 'addLibrarianPage.html')

def addLibrarian(request, user_id):
    if User.objects.filter(id=user_id).exists() and request.user.is_superuser:
        user=User.objects.get(id=user_id)
        user.is_staff=True
        user.save()
        return render(request, 'addLibrarianPage.html')
    else:
        return redirect('/')

def removeLibrarian(request, user_id):
    if User.objects.filter(id=user_id).exists() and request.user.is_superuser:
        user=User.objects.get(id=user_id)
        user.is_staff=False
        user.save()
        return redirect('/librarianManage/')
    else:
        return redirect('/')

def ModifyInformation(request):
    if request.method=='POST':
        password=request.POST.get('password')
        newPassword1=request.POST.get('newPassword1')
        newPassword2=request.POST.get('newPassword2')
        if not check_password(password, request.user.password):
            return render(request, 'modifyInformation.html', {'msg':'密碼錯誤'})
        elif newPassword1 != newPassword2:
            return render(request, 'modifyInformation.html', {'msg':'兩次密碼輸入不同'})
        else:
            request.user.set_password(newPassword1)
            request.user.save()
            messages.success(request, '密碼修改成功，請重新登入')
            return redirect('login')
    return render(request, 'modifyInformation.html')

def addBook(request):
    if request.method=='POST':
        return render(request, 'addBook.html', locals())
    else:
        return render(request, 'addBook.html')
def bookManagePage(request):
    if request.user.is_staff:
        BookList=Book.objects.all()
        return render(request, 'bookManagePage.html',locals())
    else:
        return redirect('/')

def bookModify(request, book_id):
    if Book.objects.filter(id=book_id).exists():
        book=Book.objects.get(id=book_id)
        categories=Category.objects.all()
        if request.method=='POST':
            title=request.POST.get('title')
            available_quantity=request.POST.get('available_quantity')
            content=request.POST.get('content')
            categoryId=request.POST.get('category')
            category=Category.objects.get(id=categoryId)

            book.title=title
            book.available_quantity=available_quantity
            book.content=content
            book.category=category

            book.save()
            msg='修改成功'
            return render(request, 'bookModify.html', locals())
        else:
            return render(request, 'bookModify.html', locals())
    else:
        return redirect('/')
    
def bookHide(request, book_id):
    if Book.objects.filter(id=book_id).exists():
        book=Book.objects.get(id=book_id)
        book.isOn=False
        book.save()
        return redirect('/bookManagePage/')
    else:
        return redirect('/')
    
def bookShow(request, book_id):
    if Book.objects.filter(id=book_id).exists():
        book=Book.objects.get(id=book_id)
        book.isOn=True
        book.save()
        return redirect('/bookManagePage/')
    else:
        return redirect('/')