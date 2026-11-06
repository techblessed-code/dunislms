from django.shortcuts import render
from django.http import JsonResponse

from courses.models import Course, Instructor


def home(request):
    """Landing page.

    Interface upgrade: pass real catalog data so the homepage can show
    featured courses and live stats instead of a static bullet list.
    """
    courses = Course.objects.all()
    context = {
        "featured": courses.order_by("-id")[:3],
        "course_count": courses.count(),
        "instructor_count": Instructor.objects.count(),
        # rough "hours of learning" figure from the catalog
        "hour_count": sum(c.duration or 0 for c in courses),
    }
    return render(request, "home.html", context)


def blog(request):
    return JsonResponse({"message": "blog page - Coming Soon"})
