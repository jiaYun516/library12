# urls
from django.contrib import admin
from django.urls import path
from user_borrowAndReturn import views
from login import views as loginApp

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.homepage),
    path('book/<int:id>/',views.searchById),
    path('category/<int:category_id>/',views.searchByCategory),
    path('search/',views.search, name='search'),
    path('borrowBook/<int:book_id>',views.borrowBook, name='borrowBook'),
    path('borrowList/',views.getBorrowListByUser,name='borrowList'),
    path('needReturn/',views.getNeedReturnBook,name='needReturn'),
    path('returnBookPage/',views.returnBookPage,name="returnBookPage"),
    path('returnBook/',views.returnBook,name="returnBook"),
    path('employeeManage/', views.employeeManagePage,name='employeeManage'),

    path('login/',loginApp.logins,name='login'),
    path('register/',loginApp.register,name='register'),
    path('logout/',loginApp.logouts,name='logout'),
    
]
