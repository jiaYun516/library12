from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User

# 類型
class Category(models.Model):
    name=models.CharField(max_length=100)
    isOn=models.BooleanField(default=True)

    def __str__(self):
        return self.name

# 書
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    cover = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    available_quantity = models.PositiveIntegerField()
    publication_date = models.DateField(null=True,blank=True)
    content=models.TextField(max_length=500,null=True,blank=True)
    isOn=models.BooleanField(default=True)

    def __str__(self):
        return self.title

# 借還記錄
class BorrowingRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowing_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    actual_return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} 借閱 {self.book}"
    

