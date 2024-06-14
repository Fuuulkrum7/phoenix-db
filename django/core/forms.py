# core/forms.py
from django import forms
from app.models import Child, Worker, Role, WorkerByRole, Group, TrackType
from datetime import datetime

class AddChildForm(forms.ModelForm):
    birthday = forms.DateField(widget=forms.SelectDateWidget(years=range(2000, datetime.now().year)))
    class Meta:
        model = Child
        fields = ['name', 'surname', 'patronymic', 'birthday', 'current_group', 'gender']

class AddTutorForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['name', 'surname', 'patronymic', 'hire_date', 'dismissal_date']
        widgets = {
            'dismissal_date': forms.DateInput(attrs={'type': 'date'}),
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
        }
    def save(self, commit=True):
        worker = super().save(commit=False)
        if commit:
            worker.save()
            WorkerByRole.objects.create(
                worker_id=worker,
                level_code=Role.objects.get(level_code='T')
            )
        return worker
class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['group_name', 'track_type']