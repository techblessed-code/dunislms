from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'duration', 'description', 'instructor', 'image']
        widgets = {
            'duration': forms.NumberInput(attrs={'min': 5}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'short description'}),
            'image': forms.FileInput(attrs={'accept': 'image/*'}),
        }
