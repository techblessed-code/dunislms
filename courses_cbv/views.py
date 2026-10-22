
from django.shortcuts import render
# Class-based views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from courses.models import Course
from courses.forms import CourseForm

# ListView for courses
class CourseListView(ListView):
    # order_by keeps paginated pages stable (avoids UnorderedObjectListWarning)
    queryset = Course.objects.order_by('pk')
    template_name = 'courses_cbv/course_list.html'
    context_object_name = 'courses'
    paginate_by = 100 # Optional: Add pagination if you have many courses


# CreateView for creating a new course
# LoginRequiredMixin: mutating views require a logged-in user, matching the
# @login_required on the function-based create_course view (they were open
# to anonymous visitors before).
class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses_cbv/create_course.html'

    # success URL after creating a course, allows redirecting to the course detail page
    def get_success_url(self):
        return reverse_lazy('courses_cbv:course_detail', kwargs={'pk': self.object.pk})


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses_cbv/course_detail.html'
    context_object_name = 'course'


class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses_cbv/update_course.html'

    def get_success_url(self):
        return reverse_lazy('courses_cbv:course_detail', kwargs={'pk': self.object.pk})


class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'courses_cbv/course_confirm_delete.html'
    success_url = reverse_lazy('courses_cbv:course_list')


# Compatibility aliases for function-style imports
# e.g. from courses_cbv import views; views.createcbv
createcbv = CourseCreateView.as_view()
detailcbv = CourseDetailView.as_view()
updatecbv = CourseUpdateView.as_view()
deletecbv = CourseDeleteView.as_view()

