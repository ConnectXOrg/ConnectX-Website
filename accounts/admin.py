from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import StudentProfile, EmployerProfile, User

admin.site.register(StudentProfile)
admin.site.register(EmployerProfile)
admin.site.register(User, UserAdmin)
