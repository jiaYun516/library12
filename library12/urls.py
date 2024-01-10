# urls
from django.contrib import admin
from django.urls import path
from user_borrowAndReturn import views
from login import views as loginApp

urlpatterns = [
    #瀏覽
    path('',views.homepage),
    path('book/<int:id>/',views.searchById),
    path('category/<int:category_id>/',views.searchByCategory),
    path('search/',views.search, name='search'),
    
    #借書
    path('borrowBook/<int:book_id>',views.borrowBook, name='borrowBook'),
    path('borrowList/',views.getBorrowListByUser,name='borrowList'),
    
    # 還書
    path('needReturn/',views.getNeedReturnBook,name='needReturn'),
    path('returnBookPage/',views.returnBookPage,name="returnBookPage"),
    path('returnBook/',views.returnBook,name="returnBook"),
    
    # 書籍管理
    path('bookManagePage/',views.bookManagePage,name='bookManagePage'),
    path('addBook/',views.addBook,name='addBook'),
    path('bookModify/<int:book_id>', views.bookModify, name='bookModify'),
    path('bookHide/<int:book_id>', views.bookHide, name='bookHide'),
    path('bookShow/<int:book_id>', views.bookShow, name='bookShow'),
    path('bookDelete/<int:book_id>', views.bookDelete, name='bookDelete'),

    #分類管理
    path('categoryManagePage/',views.categoryManagePage,name='categoryManagePage'),
    path('addCategory/',views.addCategory,name='addCategory'),
    path('categoryModify/<int:category_id>', views.categoryModify, name='categoryModify'),
    path('categoryHide/<int:category_id>', views.categoryHide, name='categoryHide'),
    path('categoryShow/<int:category_id>', views.categoryShow, name='categoryShow'),
    path('categoryDelete/<int:category_id>', views.categoryDelete, name='categoryDelete'),

    # 權限
    path('librarianManage/', views.librarianManagePage,name='employeeManage'),
    path('addLibrarianPage/',views.addLibrarianPage,name='addLibrarianPage'),
    path('addLibrarian/<int:user_id>',views.addLibrarian,name='addLibrarian'),
    path('removeLibrarian/<int:user_id>',views.removeLibrarian,name='removeLibrarian'),
    path('admin/', admin.site.urls),

    # 登入註冊
    path('login/',loginApp.logins,name='login'),
    path('register/',loginApp.register,name='register'),
    path('logout/',loginApp.logouts,name='logout'),
    path('modifyInformation/',views.ModifyInformation,name='modifyInformation')
]
