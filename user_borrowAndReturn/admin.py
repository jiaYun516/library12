from django.contrib import admin
from .models import Category, Book, BorrowingRecord
# 類型
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

# 書籍
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category','available_quantity']

# 借還書
class BorrowingRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'borrowing_date', 'due_date', 'actual_return_date', 'is_returned']
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BorrowingRecord, BorrowingRecordAdmin)