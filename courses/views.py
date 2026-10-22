from django.shortcuts import get_object_or_404, redirect, render

from django.contrib.auth.decorators import login_required

from courses.forms import CourseForm
from .models import Course

# Create your views here.

def course_list(request):
    # courses = [
    #     {'id': 1, 'name': 'Introduction to python'},
    #     {'id': 2, 'name': 'Django for Beginners'},
    #     {'id': 3, 'name': 'Data Science with python'}
    #     ]
    # order_by keeps the displayed order stable across requests
    courses = Course.objects.order_by('pk')

    return render(request, 'courses/course_list.html', {'courses': courses})

def about(request):
    return render(request, "courses/about.html")

def course_table(request):
    lectures  = [
    {'id': 1, 'name': 'Introduction to python', 'tutor': 'Mr Chris', 'time': '2pm WST'},
    {'id': 2, 'name': 'Django for Beginners', 'tutor': 'Mr Peace', 'time': '12pm WST'},
    {'id': 3, 'name': 'Data Science with python', 'tutor': 'Mr Chris', 'time': '4pm WST'}
    ]

    return render (request, 'courses/courses.html', {'lectures': lectures})


@login_required
def create_course(request):

    if request.method == 'POST':
        # Handle form submission to create a new course
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # return redirect('courses:course_list') # redirect to course list after successful creation
            return redirect('courses:course_details', course_id=form.instance.id)#redirect to the newly created course details page
    else:
        form = CourseForm()

    return render(request, 'courses/create_course.html', {'form': form})

def course_details(request, course_id):
    # get_object_or_404 returns a proper 404 page for a missing course
    # instead of crashing with a 500 error (Course.DoesNotExist).
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'courses/course_details.html', {'course': course})
