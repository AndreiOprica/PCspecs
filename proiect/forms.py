from django import forms
from django.db.models import fields
from django.forms import ModelForm
from .models import Comp

class CompForm(ModelForm):
    class Meta:
        model = Comp
        fields = ("username","architecture","systemname","nocores","nothreads","maxfrq","minfrq","memory","memoryavailable","memoryused",)


