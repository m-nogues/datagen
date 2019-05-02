from django import forms
from .models import *


class ExperimentChangeListForm(forms.ModelForm):

    # here we only need to define the field we want to be editable
    hacker = forms.ModelMultipleChoiceField(queryset=Hacker.objects.all(),
                                            required=False)
    # vm = forms.ModelMultipleChoiceField(queryset=Vm.objects.all(),
    #                                     required = False)
