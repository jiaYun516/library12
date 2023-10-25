from django.contrib import admin
from .models import Account, Member, Category, Book, BorrowingRecord

# 使用者狀態
class AccountAdmin(admin.ModelAdmin):
    list_display = ['name']

# 使用者
class MemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'account']

# 類型
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

# 書籍
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'slug','available_quantity']

# 借還書
class BorrowingRecordAdmin(admin.ModelAdmin):
    list_display = ['member', 'book', 'borrowing_date', 'due_date', 'actual_return_date', 'is_returned']
    
admin.site.register(Account, AccountAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BorrowingRecord, BorrowingRecordAdmin)