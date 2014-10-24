from django import forms
from tasks.models import Task
from datetimewidget.widgets import DateTimeWidget
from datetime import datetime
import pytz

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        widgets = {
            #Use localization and bootstrap 3
            'expiration_date': DateTimeWidget(attrs={'id': 'datetime', 'required': 'required'}, 
            	usel10n = True, bootstrap_version=3),
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
        }
        fields = ['title', 'expiration_date']


