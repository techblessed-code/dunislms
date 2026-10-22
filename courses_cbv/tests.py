from django.test import TestCase
from django.urls import reverse

from courses.models import Course, Instructor


class CourseCBVTests(TestCase):

    def setUp(self):
        self.instructor = Instructor.objects.create(name='Mr Peace', bio='CBV tutor')
        self.course = Course.objects.create(
            title='CBV Sample Course',
            duration=8,
            description='Learning class-based views.',
            instructor=self.instructor,
        )

    def test_course_list_view(self):
        response = self.client.get(reverse('courses_cbv:course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'CBV Sample Course')

    def test_course_detail_view(self):
        response = self.client.get(
            reverse('courses_cbv:course_detail', args=[self.course.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'CBV Sample Course')

    def test_create_update_delete_flow(self):
        # Mutating views require login (LoginRequiredMixin)
        from django.contrib.auth.models import User
        User.objects.create_user('cbvstudent', password='pass12345')
        self.client.login(username='cbvstudent', password='pass12345')

        # Create page renders
        response = self.client.get(reverse('courses_cbv:course_create'))
        self.assertEqual(response.status_code, 200)

        # Create a course -> redirects to its detail page
        response = self.client.post(reverse('courses_cbv:course_create'), {
            'title': 'Created via CBV',
            'duration': 6,
            'description': 'Created through the class-based create view.',
            'instructor': self.instructor.pk,
        })
        new_course = Course.objects.get(title='Created via CBV')
        self.assertRedirects(
            response, reverse('courses_cbv:course_detail', args=[new_course.pk])
        )

        # Update it -> redirects back to the detail page
        response = self.client.post(
            reverse('courses_cbv:course_update', args=[new_course.pk]),
            {
                'title': 'Created via CBV (updated)',
                'duration': 7,
                'description': 'Updated through the class-based update view.',
                'instructor': self.instructor.pk,
            },
        )
        new_course.refresh_from_db()
        self.assertEqual(new_course.title, 'Created via CBV (updated)')
        self.assertRedirects(
            response, reverse('courses_cbv:course_detail', args=[new_course.pk])
        )

        # Delete it -> redirects back to the list and the row is gone
        response = self.client.post(
            reverse('courses_cbv:course_delete', args=[new_course.pk])
        )
        self.assertRedirects(response, reverse('courses_cbv:course_list'))
        self.assertFalse(Course.objects.filter(pk=new_course.pk).exists())

    def test_anonymous_create_is_redirected_to_login(self):
        response = self.client.get(reverse('courses_cbv:course_create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/users/login', response.url)
