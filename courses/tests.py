
from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from .models import Course


class CourseTests(TestCase):

    # This test checks if a course can be created with the correct duration
    def test_course_creation(self):
        course = Course.objects.create(title='Test Dunis Developer Course', duration=10)
        self.assertEqual(course.duration, 10)

    # This test checks if the course list page is working
    def test_course_list_view(self):
        response = self.client.get(reverse('courses:course_list')) # Send a fake GET request
        self.assertEqual(response.status_code, 200) # Check if the page loads (status 200)
        self.assertContains(response, "No courses available") # Check for a message on that page

    def test_invalid_course_title(self):
        response = self.client.post(reverse('courses:create_course'), {
            'title': '', # Empty title should trigger an error
            'duration': 5
        })
        self.assertFormError(response, 'form', 'title', 'This field is required.')
