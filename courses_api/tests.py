from django.test import TestCase
from django.urls import reverse

from courses.models import Course, Instructor


class CourseAPITests(TestCase):

    def setUp(self):
        self.instructor = Instructor.objects.create(name='Mr API', bio='REST tutor')
        self.course = Course.objects.create(
            title='API Sample Course',
            duration=4,
            description='Testing the REST endpoints.',
            instructor=self.instructor,
        )

    def test_list_courses(self):
        response = self.client.get(reverse('course_crud_api'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'API Sample Course')

    def test_create_detail_update_delete(self):
        # POST creates a course
        response = self.client.post(reverse('course_crud_api'), {
            'title': 'Created via API',
            'duration': 3,
            'description': 'Created through the REST API.',
            'instructor': self.instructor.pk,
        })
        self.assertEqual(response.status_code, 201)
        pk = response.json()['id']

        # GET retrieves it
        response = self.client.get(reverse('course_detail_api', args=[pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'Created via API')

        # PATCH updates it
        response = self.client.patch(
            reverse('course_detail_api', args=[pk]),
            {'title': 'Updated via API'},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'Updated via API')

        # DELETE removes it
        response = self.client.delete(reverse('course_detail_api', args=[pk]))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Course.objects.filter(pk=pk).exists())

    def test_missing_course_returns_404(self):
        response = self.client.get(reverse('course_detail_api', args=[9999]))
        self.assertEqual(response.status_code, 404)
