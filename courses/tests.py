
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Category, Course, Instructor


class CourseTests(TestCase):

    def setUp(self):
        self.instructor = Instructor.objects.create(name='Mr Chris', bio='Lead tutor at Dunistech')

    # This test checks if a course can be created with the correct duration
    def test_course_creation(self):
        # description and instructor are required (NOT NULL) fields, so they
        # must be provided - the original test crashed with IntegrityError.
        course = Course.objects.create(
            title='Test Dunis Developer Course',
            duration=10,
            description='A test course about building things.',
            instructor=self.instructor,
        )
        self.assertEqual(course.duration, 10)

    # This test checks if the course list page is working
    def test_course_list_view(self):
        response = self.client.get(reverse('courses:course_list')) # Send a fake GET request
        self.assertEqual(response.status_code, 200) # Check if the page loads (status 200)
        self.assertContains(response, "No courses available") # Check for a message on that page

    # An empty title must re-render the form with an error instead of saving
    def test_invalid_course_title(self):
        user = User.objects.create_user('student', password='pass12345')
        self.client.force_login(user)  # create_course is @login_required
        response = self.client.post(reverse('courses:create_course'), {
            'title': '', # Empty title should trigger an error
            'duration': 5
        })
        # Django 6.0 signature: pass the bound form object from the response
        # context (older tutorials used assertFormError(response, 'form', ...)).
        self.assertFormError(response.context['form'], 'title', 'This field is required.')

    # Requesting a course that does not exist must return 404, not crash
    def test_course_details_missing_returns_404(self):
        response = self.client.get(reverse('courses:course_details', args=[9999]))
        self.assertEqual(response.status_code, 404)

    # Category.__str__ used to return a nonexistent attribute and crashed
    def test_category_str(self):
        category = Category.objects.create(
            name='Web Development', duration=12, description='HTML, CSS, JS'
        )
        self.assertEqual(str(category), 'Web Development')
