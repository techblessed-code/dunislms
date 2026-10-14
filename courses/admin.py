from django.contrib import admin

# Register your models here.
from .models import Course, Instructor, Category

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'instructor')
    search_fields = ('title', 'description')
    list_filter = ('instructor',)



@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('name', 'course_count')
    search_fields = ('name',)


    def course_count(self, obj):
        return obj.course_set.count()
    


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration')
    search_fields = ('name', 'description')
    list_filter = ('name',)

    

