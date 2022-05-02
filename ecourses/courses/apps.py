from django.apps import AppConfig

# Mình sẽ đưa giá trị name của class vào bên trong INSTALLED_APPS là 'courses.apps.CoursesConfig'
class CoursesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'courses'
