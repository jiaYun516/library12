from user_borrowAndReturn.models import Book, Category, BorrowingRecord
from django.db.models import Count, F
from django.shortcuts import render, redirect, HttpResponse,  get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import check_password

def identity(user):
    if user.is_superuser:
        return "管理"
    elif user.is_staff:
        return "圖書員"
    else:
        return "讀者"

def homepage(request):
    books = Book.objects.filter(isOn=True).annotate(borrow_count=Count('borrowingrecord')).order_by('-borrow_count', 'title')
    if request.user.is_active:
        is_superuser_staff=request.user.is_superuser or request.user.is_staff
        identityName=identity(request.user)
        return render(request, 'homePage.html', locals())
    else:
        is_superuser_staff=False
        return render(request, 'homePage.html', locals())

def searchById(request, id):
    book=Book.objects.get(id=id, isOn=True)
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


def searchByCategory(request, category_id):
    # try:
        category = Category.objects.filter(id=category_id).first()
        books=Book.objects.filter(category=category, isOn=True).annotate(borrow_count=Count('borrowingrecord')).order_by('-borrow_count', 'title')
        if books:
            return render(request, 'searchByCategoryPage.html', {'books':books,'category':category})
        else:
            return render(request, 'searchByCategoryPage.html', {'msg':'此類別暫無書籍','category':category})
    # except:
        # return redirect('/')

def search(request):
    kw = request.GET.get('keyWord')
    books = Book.objects.filter(title__icontains=kw, isOn=True) | Book.objects.filter(author__icontains=kw, isOn=True)
    return render(request, 'search_results.html', {'books': books, 'keyWord': kw})

def borrowBook(request, book_id):
    if request.user.is_active:
        book = Book.objects.get(id=book_id, isOn=True)
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
            return render(request, 'borrowBook.html', {'borrowing_record': borrowing_record,'msg':'借閱成功！'})
        else:
            return render(request, 'borrowBook.html', {'msg': '圖書暫不可借'})
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
                                                  due_date__lte=three_days_later,
                                                  due_date__gte=day_now).order_by('due_date')  #__gte大於等於 __lte小於等於
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
    
def bookManagePage(request):
    if request.user.is_superuser:
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
            cover=request.POST.get('cover')
            publication_date=request.POST.get('publication_date')
            category=Category.objects.get(id=categoryId)
            

            book.title=title
            book.cover=cover
            book.publication_date=publication_date
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

def addBook(request):
    if request.method=='POST':
        title=request.POST.get('title')
        author=request.POST.get('author')
        cover=request.POST.get('cover')
        available_quantity=request.POST.get('available_quantity')
        publication_date=request.POST.get('publication_date')
        content=request.POST.get('content')
        categoryId=request.POST.get('category')
        category=Category.objects.get(id=categoryId)
        book=Book.objects.create(title=title,author=author,
                                 cover=cover,available_quantity=available_quantity,
                                 publication_date=publication_date,content=content,
                                 category=category)
        msg='新增成功'
        return render(request, 'addBook.html', locals())
    else:
        return render(request, 'addBook.html')

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

def bookDelete(request, book_id):
    # try:
        book=Book.objects.filter(id=book_id).first()
        borrowingRecord=BorrowingRecord.objects.filter(book=book, is_returned=False)
        if borrowingRecord:
            q='圖書刪除錯誤'
            msg='尚有用戶借閱此無法刪除，可以選擇隱藏書籍哦'
            k='book'
            return render(request, 'manageErrorMsgPage.html', locals())
        else:
            book.delete()
            return redirect('/bookManagePage/')
    # except:
    #     return redirect('/')

def categoryManagePage(request):
    if request.user.is_superuser:
        categoryList=Category.objects.all()
        return render(request, 'categoryManagePage.html',locals())
    else:
        return redirect('/')

def addCategory(request):
    if request.method=='POST':
        name=request.POST.get('name')
        category=Category.objects.create(name=name)
        msg='新增成功'
        return render(request, 'addCategory.html', locals())
    return render(request, 'addCategory.html', locals())

def categoryModify(request, category_id):
    category=Category.objects.filter(id=category_id).first()
    if category:
        if request.method=='POST':
            name=request.POST.get('name')
            category.name=name
            category.save()
            msg='修改成功'
            return render(request, 'categoryModify.html', locals())
        else:
            return render(request, 'categoryModify.html', locals())
    else:
        return redirect('/')

def categoryHide(request, category_id):
    category=Category.objects.filter(id=category_id).first()
    if category:
        category.isOn=False
        category.save()
        return redirect('/categoryManagePage/')
    else:
        return redirect('/')
    
def categoryShow(request, category_id):
    category=Category.objects.filter(id=category_id).first()
    if category:
        category.isOn=True
        category.save()
        return redirect('/categoryManagePage/')
    else:
        return redirect('/')

def categoryDelete(request, category_id):
    try:
        category=Category.objects.filter(id=category_id).first()
        book=Book.objects.filter(category=category)
        if book:
            q='分類刪除錯誤'
            msg='尚有書籍在此分類無法刪除，可以選擇隱藏分類哦'
            k='category'
            return render(request, 'manageErrorMsgPage.html', locals())
        else:
            category.delete()
            return redirect('/categoryManagePage/')
    except:
        return redirect('/')
