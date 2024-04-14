from typing import Any, Mapping
from django.core.files.base import File
from django.db.models.base import Model
from django.forms import ModelForm
from django.forms.utils import ErrorList
from .models import Job


class JobForm(ModelForm):
    """Represnet the Job as a form
        to let the employer post a new job"""

    class Meta:
        model = Job
        exclude = ['employer',]
        widgets = {
        }
        labels = {
            'exp_level': 'Exp Level for this job'
        }