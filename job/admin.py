from django.contrib import admin
from .models import User, Student, Company, Internship, Application

admin.site.site_header = "Job Management"
admin.site.index_title = "Administration Job Management" 


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "is_student", "is_company", )
    fields = ("username", "is_student", "is_company")


class StudentAdmin(admin.ModelAdmin):
    list_display = ("user", "last_name", "academic_level", "phone", "cv", "transcript")
    fields = ("user", "last_name", "academic_level", "phone", "cv", "transcript")

class CompanyAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "description", "website", "contact_person", "contact_email")
    fields = ("user", "name", "description", "website", "contact_person", "contact_email")

class InternshipAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "location", "start_date", "end_date", "requirements")
    fields = ("title", "description", "location", "start_date", "end_date", "requirements", "company")

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("student", "internship", "status")
    fields = ("student", "internship", "status")



admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Internship, InternshipAdmin)
admin.site.register(Application, ApplicationAdmin)