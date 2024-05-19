# core/forms/visit_forms.py
from django import forms
from app.models import Visits

## \class VisitForm
## \brief A form for recording a child's visit to a lesson.
class VisitForm(forms.ModelForm):
    visited = forms.BooleanField(initial=True, required=False)  # Checkbox to indicate if the child visited.
    reason = forms.CharField(widget=forms.Textarea, required=False)  # Text area for reasons if the child did not visit.

    class Meta:
        model = Visits
        fields = ['lesson_date', 'description', 'visited', 'reason']  # Fields to include in the form.
        widgets = {
            'lesson_date': forms.HiddenInput(),  # Hidden input for lesson date.
            'description': forms.HiddenInput(),  # Hidden input for description.
        }
