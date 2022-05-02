from django.contrib.auth.models import AbstractUser
from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
# Model là nơi tạo ra các class để ánh xạ xuống CSDL
# AbstracUser nghĩa là nó có sẵn một bộ chứng thực sẵn
class User(AbstractUser): # khi thay đổi class User thì phải thêm AUTH_USER_MODEL = 'courses.User' vào bên trong Setting
    # Thêm avatar cho người dùng
    # Khi sử dụng ImageField thì cài pip install pillow
    avatar = models.ImageField(upload_to='uploads/%Y/%m')

class Category(models.Model): # courses_category
    # Tạo thuộc tính name có kiểu charField với điều kiện tối đa 100 ký tự, không được phép null, unique nghĩa là không được có 2 cái category name trùng nhau
    name = models.CharField(max_length=100,null=False, unique=True)

    # chuyển đổi thành một string xuất hiện lên màn hình
    def __str__(self): # self đại diện cho this trỏ tới thuộc tính name và trả về 1 string
        return self.name

class ItemBase(models.Model):
    class Meta:
        abstract = True
    subject = models.CharField(max_length=255, null=False)
    # đường dẫn lưu ảnh Media_ROOT + upload_to
    image = models.ImageField(upload_to='courses/%Y/%m', default=None)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.subject

# Class Course kế thừa từ ItemBase => models.Model chuyển thành ItemBase
class Course(ItemBase):
    class Meta:
        # unique_together nghĩa là 2 giá trị này gộp lại phải là unique
        # trong cùng 1 category không được phép trùng subject
        # unique_together = ('subject', 'category')
        # ordering nghĩa là sắp xếp tăng dần hay giảm dần khi truy vấn theo trường nào đó
        # VD: sắp theo subject và created_date
        ordering = ['subject', 'created_date']
    # null = False nếu không khai báo mặc định cũng là false
    # null được phép, rỗng được phép (blank = true)
    description = models.TextField(null=True, blank=True)
    # dữ liệu ngày tháng ngay khi mình tạo
    # DataTimeField cần luôn giờ tạo, DameTime thì không có giờ tạo
    # auto_now_add nghĩa là nó sẽ tự động lấy thời gian tạo để gán vào cho biến created_date mà mình không cần phải quan tâm nữa
    # created_date = models.DateTimeField(auto_now_add=True)
    # auto_now bất chấp mỗi khi có sự thay đổi thuộc tính gì của Course thì biến updated_date sẽ tự động được cập nhật thành now
    # updated_date = models.DateTimeField(auto_now=True)
    # Xoá logic nhưng nó vẫn còn thì sử dụng trường này active 
    # default=True nghĩa là lúc tạo thì nó luôn luôn là True
    # active = models.BooleanField(default=True)
    # Cài đặt thuộc tính khoá ngoại Category chính là bảng mà nó tham chiếu tới, tham số thứ 2 là khi delete khoá học này thì sẽ xử lý ra sao
    # on_delete=models.CASCADE nghĩa là khi xoá Category thì toàn bộ course cũng bị xoá theo
    # category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # on_delete=models.SET_NULL, null=True có nghĩa là khi category bị xoá thì trường category ở Course sẽ là NULL
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

# Class Lesson kế thừa từ ItemBase => models.Model chuyển thành ItemBase
class Lesson(ItemBase):
    class Meta:
        # Trong cùng một course không được phép trùng subject
        unique_together = ('subject', 'course')
        # Khi ta muốn thay đổi tên bảng trong CSDL thì dùng db_table thay thế cho Course_lesson
        # db_table = '...'
        # Khi ta muốn thay đổi tên app thì dùng app_labels. Mặc định sẽ là courses
        # app_label = '...'
    content = RichTextField()
    # upload_to là nơi mình sẽ upload vào đó. Thường là thư mục static sẽ chứa ảnh. %Y là địa diện cho thời gian theo năm, %m đại diện cho thời gian theo tháng
    # 3 thuộc tính bên dưới mình comment đi vì giờ nó sẽ kế thừa từ ItemBase => models.Model
    # image = models.ImageField(upload_to='lessons/%Y/%m')
    # created_date = models.DateTimeField(auto_now_add=True)
    # updated_date = models.DateTimeField(auto_now=True)
    # active = models.BooleanField(default=True)
    # on_delete=models.SET_NULL: khi Course bị xoá thì nó sẽ xét trường course thành NULL
    # on_delete=models.SET_DEFAULT: khi Course bị xoá đi mà ta muốn Lesson sẽ thuộc vào một Course mặc định thì ta dùng SET_DEFAULT
    # on_delete=models.CASCADE: khi xoá Course thì toàn bộ Lesson cũng bị xoá theo
    # on_delete=models.PROTECT: khi Course có những Lesson thì không được phép xoá Course đó
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    # Một bài học có nhiều tags thì dùng models.ManyToManyField. Nếu class Tag ở bên dưới thì để trong dấu '', Nếu class Tag ở trên thì không cần dấu ''
    # Đối với các lesson có rồi trước khi thêm trường tags thì Tag mới thêm vào sẽ được xử lý ntn. Do có quan hệ ManyToMany nên trogn CSDL sẽ tạo ra 1 bảng course_lesson_tags
    # tags = models.ManyToManyField('Tag', blank=True, null=True)
    tags = models.ManyToManyField('Tag', related_name="lessons", blank=True, null=True)

# Demo quan hệ ManyToMany
class Tag(models.Model):
    # Unique=True để tránh tạo ra 2 cái trùng nhau
    name = models.CharField(max_length=50, unique=True)

    # Khi in ra thì lấy tên
    def __str__(self):
        return self.name