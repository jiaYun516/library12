from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

# 使用者狀態
class Account(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
# 使用者
class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# 類型
class Category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

# 書
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    cover = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    available_quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.title

# 借還記錄
class BorrowingRecord(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowing_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(default=timezone.now()+timezone.timedelta(days=60))
    actual_return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.member} 借閱 {self.book}"
