'''
django自動讀取後base.html可以直接調用這個方法不需要透過url
這樣就可以減少側邊欄增刪時修改的工作量><

功能：側邊跳轉書籍類型的鏈接
使用方式：
{% getAllCategoryForMenu as categories %}   獲取資料
{% for category in categories %}    遍歷資料
    <li><a href="category/{% category.id %}/">{{ category.name }}</a></li>  變成html格式
{% endfor %}
'''


from django import template
from user_borrowAndReturn.models import Category

register = template.Library()

@register.simple_tag
def get_menu_categories():
    return Category.objects.all()