"""Seed the LMS catalog with the standard demo courses.

Why this exists: db.sqlite3 is gitignored (see .gitignore), so a fresh
clone starts with an EMPTY course table and the homepage shows nothing.
Run this once after `migrate` to reproduce the full demo catalog:

    python manage.py seed_courses

It is idempotent (get_or_create) - running it twice does no harm.
It also removes the practice entries typed while testing the forms
(the duplicate "English" and "math/Mathematics" courses), because the
catalog of this academy is software / full-stack courses only.
"""

from django.core.management.base import BaseCommand

from courses.models import Course, Instructor, Category


# (title, duration_hours, description, instructor_name)
COURSES = [
    ("Introduction to Web Development", 12,
     "Learn HTML, CSS and JavaScript from zero and build your first responsive website.",
     "Mr. Chris"),
    ("Python Programming Masterclass", 20,
     "From variables to functions, loops and files - a complete path to thinking in Python.",
     "Mr. Chris"),
    ("Django Web Development Bootcamp", 24,
     "Build real web apps with Django: models, views, templates, auth and deployment.",
     "Mr. Peace"),
    ("JavaScript Fundamentals", 14,
     "Master variables, DOM manipulation, events and fetch APIs with hands-on projects.",
     "Mr. Peace"),
    ("Database Design with SQL", 10,
     "Design clean relational databases: tables, joins, indexes and normalisation.",
     "Mr. Peace"),
    ("Git and Version Control", 6,
     "Track, branch and merge your code confidently - the workflow every developer needs.",
     "Mr. Chris"),
    ("REST API Development with Django", 16,
     "Design, secure and document REST APIs with Django REST Framework and JWT.",
     "Mr. Peace"),
    ("Cybersecurity Basics", 8,
     "Understand threats, safe passwords, HTTPS and how to protect your applications.",
     "Mr. Chris"),
    ("Data Structures and Algorithms", 18,
     "Lists, stacks, queues, trees and the interview-ready thinking behind them.",
     "Mr. Chris"),
    ("Cloud Computing Fundamentals", 10,
     "Servers, containers and deployment - how apps really run in production.",
     "Mr. Peace"),
]

INSTRUCTORS = {
    "Mr. Chris": "Lead tutor at Dunistech Academy. Passionate about making code simple for beginners.",
    "Mr. Peace": "Backend engineer and tutor. Loves Django, APIs and clean database design.",
}

CATEGORIES = [
    ("Web Development", 12, "Front-end and full-stack web tracks."),
    ("Programming", 20, "Core programming and computer science."),
]


class Command(BaseCommand):
    help = "Seed the demo course catalog (and remove duplicate English practice entries)."

    def handle(self, *args, **options):
        # 1. Clean up the junk typed while testing the forms.
        #    Rule: only software / full-stack courses belong in this catalog,
        #    so the English and math practice entries always get removed.
        doomed = Course.objects.filter(
            title__iexact="english"
        ) | Course.objects.filter(title__in=["math", "Mathematics"])
        removed = doomed.count()
        doomed.delete()

        # 2. Instructors and categories the courses hang off.
        instructors = {}
        for name, bio in INSTRUCTORS.items():
            obj, _ = Instructor.objects.get_or_create(name=name, defaults={"bio": bio})
            instructors[name] = obj

        for name, duration, description in CATEGORIES:
            Category.objects.get_or_create(
                name=name, defaults={"duration": duration, "description": description}
            )

        # 3. The catalog itself (get_or_create = safe to re-run).
        created = 0
        for title, duration, description, instructor in COURSES:
            _, was_created = Course.objects.get_or_create(
                title=title,
                defaults={
                    "duration": duration,
                    "description": description,
                    "instructor": instructors[instructor],
                },
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(
            f"Removed {removed} duplicate English course(s); "
            f"created {created} course(s). "
            f"Catalog now holds {Course.objects.count()} course(s)."
        ))
