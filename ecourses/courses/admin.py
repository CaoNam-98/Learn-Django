from django.contrib import admin
from django.utils.html import mark_safe
from .models import *
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.urls import path
from django.template.response import TemplateResponse
from django.db.models import Count

class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Lesson
        fields = '__all__' # __all__ lấy tất cả các trường của lesson mà nó tương tác

class LessonTagInlineAdmin(admin.TabularInline):
    model = Lesson.tags.through

class LessonAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('/static/css/main.css',)
        }
    inlines = [LessonTagInlineAdmin,]
    # ckeditor
    form = LessonForm
    # Trường hiển thị
    list_display = ["id", "subject", "created_date", "active", "course"]
    # List filter
    list_filter = ["subject", "course__subject"]
    # Trường tìm kiếm
    search_fields = ["subject", "created_date", "course__subject"]
    readonly_fields = ["avatar"] # avatar sẽ chọc xuống def avatar. Lưu ý không đặt image vì nó sẽ trùng tên với image trogn class Lesson

    def avatar(self, lesson):
        # mark_safe là trả về một thẻ html và lưu ý khi lên server thì phải có /static để nó gắn cái host vào
        # lesson.image.name là lấy ra name (value) của image
        return mark_safe(
            "<img src='/static/{img_url}' alt='{alt}' width='120px' />"
            .format(img_url=lesson.image.name, alt=lesson.subject)
            )

class LessonInline(admin.StackedInline):
    model = Lesson 
    pk_name = 'course' # course là Foreign của Lesson

class CourseAdmin(admin.ModelAdmin):
    inlines = (LessonInline,)
# Register your models here.
# Admin để cấu hình các thành phần của trang admin

class CourseAppAdminSite(admin.AdminSite):
    site_header = 'HE THONG QUAN LY KHOA HOC'

    def get_urls(self):
        return [
            path('course-stats/', self.course_stats)
        ] + super().get_urls()

    def course_stats(self, request): # view luôn có 1 đối số là request
        course_count = Course.objects.count()
        # đếm trong khoá họcnayf có bao nhiêu Lesson. lessons chính là related_name, nếu không có related_name thì dùng lesson_set
        # values("id", "subject", "lesson_count") là lấy ra thông tin id, subject, lesson_count của khoá học
        stats = Course.objects.annotate(lesson_count=Count('lessons')).values("id", "subject", "lesson_count")
        return TemplateResponse(request, 'admin/course-stats.html', {
            'course_count': course_count,
            'stats': stats
        })

admin_site = CourseAppAdminSite('mycourse')

admin_site.register(Category)
admin_site.register(Course, CourseAdmin)
# Truyền LessonAdmin xuống làm tham số thứ 2 để Custom lại trang admin
admin_site.register(Lesson, LessonAdmin)