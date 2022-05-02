# Nơi này tạo ra các url cho app
from django.contrib import admin
from django.urls import path, re_path
# . là đại diện cho thư mục hiện tại
from . import views
from .admin import admin_site

urlpatterns = [
    # name dùng để phân giải đường dẫn ra và là optional
    path('', views.index, name="index"),
    # ta dùng / phía sau do URL cha đã có / rồi
    # name mình để sau này mình sẽ dùng nó
    path('welcome/<int:year>/', views.welcome, name="welcome"),
    # re_path dùng cho biểu thức chính quy nhận vào tham số year và nhận vào tham sô 0-9
    # và có tối đa là 2 chữ số, tối thiểu là 1 chữ số
    # Nếu để {4} là có 4 chữu số
    re_path(r'welcome2/(?P<year>[0-9]{1,2})/$', views.welcome2, name="welcome2"),
    path('test/', views.TestView.as_view()),
    path('admin/', admin_site.urls)
]