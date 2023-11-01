# urls
from django.contrib import admin
from django.urls import path
from user_borrowAndReturn import views

urlpatterns = [
    path('/admin/', admin.site.urls),
    path('',views.homepage),
    path('book/<int:id>/',views.searchById),
    path('category/<int:category_id>/',views.searchByCategory)
]
