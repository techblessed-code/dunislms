from django.db import models

# Create your models here.
class Instructor(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=200)
    duration = models.IntegerField(help_text="Duration in hours")
    description = models.TextField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='courses/', null=True, blank=True)

    def __str__(self):

        return self.title
    
    
class Category(models.Model):
    name = models.CharField(max_length=200)
    duration = models.IntegerField(help_text="Duration in hours")
    description = models.TextField()



    def __str__(self):
        # Bug fix: this used to return self.category, which does not exist on
        # this model - any str(category) call (admin lists, forms, shell)
        # crashed with AttributeError. The model's text field is 'name'.
        return self.name
    