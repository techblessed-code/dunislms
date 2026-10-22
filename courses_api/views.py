from rest_framework import generics

from courses.models import Course
from .serializers import CourseSerializer


# NOTE: The original CourseCRUDAPIView - a plain APIView that only implemented
# GET - is commented out because it duplicated the list endpoint below while
# accepting no writes. CourseCreateAPIView (ListCreateAPIView) now serves the
# same GET (list) and adds POST (create), with browsable-API docs for free.
#
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
#
#
# class CourseCRUDAPIView(APIView):
#
#     def get(self, request):
#         courses = Course.objects.all()
#         serializer = CourseSerializer(courses, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


class CourseCreateAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
